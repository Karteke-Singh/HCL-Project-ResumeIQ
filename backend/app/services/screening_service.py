
import json
from typing import Any, Dict

from backend.app.schemas import (
    JobRequirements,
    ParsedProfile,
    ScoringWeights,
)
from backend.app.services.resume_parser import resume_parser_v1
from backend.app.services.jd_analyzer import jd_analyzer
from backend.app.services.rule_filter import rule_filter
from backend.app.services.semantic_scorer import semantic_scorer
from backend.app.services.explainer import explainer_service
from backend.app.services.fusion import fusion_engine
from backend.app.ai.llm_client import llm_client


def _parse_json(value: str, default: dict) -> dict:
    """Read JSON stored in the database safely."""
    try:
        parsed = json.loads(value) if value else default
        return parsed if isinstance(parsed, dict) else default
    except (json.JSONDecodeError, TypeError):
        return default


def _build_requirements(job: Any) -> JobRequirements:
    """Load saved job requirements, or analyze the job description."""
    saved = _parse_json(job.requirements_json, {})

    if saved:
        return JobRequirements.model_validate(saved)

    return jd_analyzer.analyze(job.jd_text)


def _build_weights(job: Any) -> ScoringWeights:
    """Load configured scoring weights or use schema defaults."""
    saved = _parse_json(job.weights_json, {})
    return ScoringWeights.model_validate(saved)


class ScreeningService:
    """Coordinates resume parsing, scoring, and explanation."""

    def screen_resume(self, job: Any, raw_text: str) -> Dict[str, Any]:
        if not raw_text or not raw_text.strip():
            raise ValueError("Resume text cannot be empty.")

        # 1. Parse the resume.
        profile: ParsedProfile = resume_parser_v1.parse(raw_text)

        # 2. Load the job's requirements and scoring weights.
        requirements = _build_requirements(job)
        weights = _build_weights(job)

        # 3. Evaluate mandatory requirements.
        rule_result = rule_filter.evaluate(profile, requirements)

        # 4. Calculate resume-to-job text similarity.
        semantic_score = semantic_scorer.compute_similarity(
            resume_text=raw_text,
            jd_text=job.jd_text,
            profile=profile,
            requirements=requirements,
        )

        # 5. Calculate the experience score.
        required_years = requirements.minimum_experience_years

        if required_years > 0:
            experience_score = min(
                1.0,
                max(0.0, profile.experience_years / required_years),
            )
        else:
            experience_score = 1.0

        # 6. Ask the configured LLM provider for a fit rating.
        profile_summary = (
            f"Summary: {profile.professional_summary or 'Not provided'}\n"
            f"Skills: {', '.join(profile.skills)}\n"
            f"Experience: {profile.experience_years} years\n"
            f"Education: {profile.education or 'Not provided'}\n"
            f"Projects: {profile.projects}\n"
            f"Certifications: {', '.join(profile.certifications)}"
        )

        requirements_summary = (
            f"Must-have skills: {requirements.must_have_skills}\n"
            f"Nice-to-have skills: {requirements.nice_to_have_skills}\n"
            f"Minimum experience: "
            f"{requirements.minimum_experience_years} years\n"
            f"Preferred education: {requirements.preferred_education}"
        )

        fit_result = llm_client.rate_fit(
            profile_summary=profile_summary,
            requirements_summary=requirements_summary,
            passed_hard_rules=rule_result["passed"],
        )

        llm_fit_score = min(
            1.0,
            max(0.0, float(fit_result["fit_rating_0_to_10"]) / 10.0),
        )

        # 7. Combine component scores.
        scores = fusion_engine.fuse(
            rule_score=rule_result["rule_score"],
            semantic_score=semantic_score,
            experience_score=experience_score,
            llm_fit_score=llm_fit_score,
            passed_hard_requirements=rule_result["passed"],
            weights=weights,
        )

        # 8. Generate an explanation with resume-based evidence.
        matched_skills = rule_result["matched_must_haves"]
        missing_skills = rule_result["missing_must_haves"]

        explanation_result = explainer_service.generate_explanation(
            profile=profile,
            requirements=requirements,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            passed_rules=rule_result["passed"],
            raw_text=raw_text,
        )

        # 9. Return results without writing to the database.
        return {
            "candidate_id": profile.candidate_id,
            "display_name": profile.name or "Name not extracted",
            "job_id": job.id,
            "job_title": job.title,
            "scores": scores.model_dump(),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "experience_passed": rule_result["experience_passed"],
            "llm_reason": fit_result["one_line_reason"],
            "explanation": explanation_result["explanation"],
            "evidence_snippets": explanation_result["evidence_snippets"],
            "warnings": [
                "Verify extracted candidate information and evidence.",
                "Scores support human review; they do not make hiring decisions.",
            ],
        }


screening_service = ScreeningService()
