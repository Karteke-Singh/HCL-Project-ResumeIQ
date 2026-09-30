import re
from typing import Dict, Any


class PIIMasker:
    """
    Masks Personally Identifiable Information (PII) and demographic markers:
    1. Names
    2. Gender-indicative pronouns
    3. University / College names
    4. Emails and phone numbers
    """

    PRONOUN_MAP = {
        r"\bhe\b": "they",
        r"\bshe\b": "they",
        r"\bhim\b": "them",
        r"\bher\b": "them",
        r"\bhis\b": "their",
        r"\bhers\b": "theirs",
        r"\bhimself\b": "themself",
        r"\bherself\b": "themself"
    }

    def mask_text(self, text: str, candidate_display_id: str = "CANDIDATE") -> str:
        masked = text

        # Mask Emails
        masked = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL_MASKED]", masked)

        # Mask Phone numbers
        masked = re.sub(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", "[PHONE_MASKED]", masked)

        # Mask Candidate Name in headers
        masked = re.sub(r"(CANDIDATE\s+NAME:\s*)([^\n\r]+)", rf"\1[NAME_MASKED - {candidate_display_id}]", masked, flags=re.IGNORECASE)

        # Mask Institutional brand names
        masked = re.sub(
            r"\b[A-Z][a-zA-Z\s]+(?:University|College|Institute|Academy|School)\b",
            "[ACADEMIC_INSTITUTION_MASKED]",
            masked
        )

        # Mask gender pronouns (case-preserving substitution)
        for pattern, replacement in self.PRONOUN_MAP.items():
            masked = re.sub(pattern, replacement, masked, flags=re.IGNORECASE)

        return masked


pii_masker = PIIMasker()
