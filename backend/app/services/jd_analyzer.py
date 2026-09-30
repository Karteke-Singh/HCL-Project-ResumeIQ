import re
from typing import List, Dict, Any, Optional
from backend.app.schemas import JobRequirements
from backend.app.services.resume_parser import ALL_TAXONOMY_SKILLS, resume_parser_v1


class JDAnalyzer:
    """
    Analyzes job descriptions to extract must-have skills, nice-to-have skills,
    minimum experience threshold, and preferred education.
    """

    def analyze(self, jd_text: str) -> JobRequirements:
        lower_text = jd_text.lower()

        # Split must-have vs nice-to-have sections if headers exist
        must_have = []
        nice_to_have = []

        must_have_match = re.search(r"(?:must[- ]have|required|mandatory|qualifications)[\s\S]*?(?=(?:nice[- ]to[- ]have|preferred|desired|responsibilities|\Z))", jd_text, re.IGNORECASE)
        nice_to_have_match = re.search(r"(?:nice[- ]to[- ]have|preferred|desired|plus)[\s\S]*?(?=(?:responsibilities|duties|\Z))", jd_text, re.IGNORECASE)

        if must_have_match:
            must_have = self._extract_skills_from_chunk(must_have_match.group(0))
        if nice_to_have_match:
            nice_to_have = self._extract_skills_from_chunk(nice_to_have_match.group(0))

        # If sections weren't explicitly delineated, fall back to global extraction
        if not must_have and not nice_to_have:
            all_found = self._extract_skills_from_chunk(jd_text)
            must_have = all_found[:5] if len(all_found) > 5 else all_found
            nice_to_have = all_found[5:] if len(all_found) > 5 else []

        # Remove duplicates from nice_to_have that appear in must_have
        nice_to_have = [s for s in nice_to_have if s not in must_have]

        # Extract minimum experience
        min_exp = 0.0
        exp_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:to\s*\d+\s*)?years?(?:\s*of)?\s*(?:relevant\s*|professional\s*)?experience", jd_text, re.IGNORECASE)
        if exp_match:
            min_exp = float(exp_match.group(1))

        # Preferred Education
        preferred_edu = "Bachelor's degree in Computer Science, Software Engineering, or related field"
        edu_match = re.search(r"(Bachelor[^\.\n\r]+|Master[^\.\n\r]+|Degree in [^\.\n\r]+)", jd_text, re.IGNORECASE)
        if edu_match:
            preferred_edu = edu_match.group(1).strip()

        return JobRequirements(
            must_have_skills=must_have,
            nice_to_have_skills=nice_to_have,
            minimum_experience_years=min_exp,
            preferred_education=preferred_edu,
            key_responsibilities=[]
        )

    def _extract_skills_from_chunk(self, text: str) -> List[str]:
        found = set()
        lower = text.lower()
        for skill in ALL_TAXONOMY_SKILLS:
            escaped = re.escape(skill)
            pattern = rf"(?<!\w){escaped}(?!\w)"
            if re.search(pattern, lower):
                found.add(resume_parser_v1._canonical_name(skill))
        return sorted(list(found))


jd_analyzer = JDAnalyzer()
