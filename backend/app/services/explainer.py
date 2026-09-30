import re
from typing import List, Dict, Any
from backend.app.schemas import ParsedProfile, JobRequirements


class ExplainerService:
    """
    Tier 3 Explainer Layer:
    - Extracts evidence citations from the resume text.
    - Compiles a transparent, human-readable rationale.
    - Protects against speculation and ensures no demographic attributes are referenced.
    """

    def generate_explanation(
        self,
        profile: ParsedProfile,
        requirements: JobRequirements,
        matched_skills: List[str],
        missing_skills: List[str],
        passed_rules: bool,
        raw_text: str
    ) -> Dict[str, Any]:
        evidence_snippets = []

        # Find evidence lines for matched skills
        text_lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
        for skill in matched_skills[:4]:
            escaped = re.escape(skill)
            for line in text_lines:
                if re.search(rf"(?<!\w){escaped}(?!\w)", line, re.IGNORECASE):
                    cleaned_line = re.sub(r"^[-\*•\d\.]+\s*", "", line).strip()
                    if len(cleaned_line) > 15 and cleaned_line not in evidence_snippets:
                        evidence_snippets.append(f"Evidence for {skill}: \"{cleaned_line[:120]}\"")
                        break

        # Construct concise rationale
        exp_status = "meets" if profile.experience_years >= requirements.minimum_experience_years else "below"
        rationale_parts = []

        if passed_rules and len(matched_skills) >= 3:
            rationale_parts.append(
                f"Candidate exhibits strong alignment with mandatory competencies ({', '.join(matched_skills[:4])}) "
                f"and {exp_status} the minimum experience threshold with {profile.experience_years} years."
            )
        elif not passed_rules and profile.experience_years < requirements.minimum_experience_years:
            rationale_parts.append(
                f"Candidate possesses relevant technical skills ({', '.join(matched_skills[:3])}), "
                f"but does not meet the minimum professional experience requirement ({profile.experience_years} yrs vs {requirements.minimum_experience_years} yrs required)."
            )
        else:
            rationale_parts.append(
                f"Candidate profile has limited overlap with core technical requirements. "
                f"Gaps identified in key must-have competencies: {', '.join(missing_skills[:3])}."
            )

        if profile.education and profile.education.degree:
            rationale_parts.append(f"Education: {profile.education.degree} in {profile.education.field_of_study or 'relevant discipline'}.")

        return {
            "explanation": " ".join(rationale_parts),
            "evidence_snippets": evidence_snippets[:3]
        }


explainer_service = ExplainerService()
