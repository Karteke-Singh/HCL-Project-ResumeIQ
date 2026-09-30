from typing import List, Tuple, Dict, Any
from backend.app.schemas import ParsedProfile, JobRequirements


class RuleFilter:
    """
    Tier 1 Rule Layer:
    - Pass/Fail gate on minimum experience years
    - Mandatory skill overlap computation
    - Hard gate outcome
    """

    def evaluate(self, profile: ParsedProfile, requirements: JobRequirements) -> Dict[str, Any]:
        must_haves = set(s.lower() for s in requirements.must_have_skills)
        candidate_skills = set(s.lower() for s in profile.skills)

        # Matched and missing must-haves
        matched_must_haves = [s for s in requirements.must_have_skills if s.lower() in candidate_skills]
        missing_must_haves = [s for s in requirements.must_have_skills if s.lower() not in candidate_skills]

        # Minimum experience check
        experience_passed = profile.experience_years >= requirements.minimum_experience_years

        # Must-have skill ratio
        skill_ratio = len(matched_must_haves) / len(must_haves) if must_haves else 1.0

        # Hard requirements pass if experience is met and at least 50% must-haves are present
        passed_hard_requirements = experience_passed and (skill_ratio >= 0.5)

        # Rule score calculation (0.0 to 1.0)
        # Experience factor (capped at 1.0)
        if requirements.minimum_experience_years > 0:
            exp_factor = min(1.0, profile.experience_years / requirements.minimum_experience_years)
        else:
            exp_factor = 1.0

        rule_score = round(0.6 * skill_ratio + 0.4 * exp_factor, 3)

        return {
            "passed": passed_hard_requirements,
            "rule_score": rule_score,
            "experience_passed": experience_passed,
            "matched_must_haves": matched_must_haves,
            "missing_must_haves": missing_must_haves,
        }


rule_filter = RuleFilter()
