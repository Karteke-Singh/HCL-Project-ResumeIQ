import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from backend.app.config import settings
from backend.app.ai.validators import extract_and_validate_json


class LLMClient:
    """
    Single Provider Adapter for LLM calls.
    Allows swapping providers (Gemini, Groq, OpenAI, Mock) via configuration
    without modifying screening business logic.
    """

    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or settings.LLM_PROVIDER).lower()
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
        self.prompts_dir = Path(__file__).resolve().parent / "prompts"

    def _read_prompt(self, template_name: str) -> str:
        prompt_file = self.prompts_dir / template_name
        return prompt_file.read_text(encoding="utf-8")

    def rate_fit(self, profile_summary: str, requirements_summary: str, passed_hard_rules: bool) -> Dict[str, Any]:
        """Calls fit rating prompt and returns rating (0-10) and one-line reason."""
        if self.provider == "mock" or not self.api_key:
            # Deterministic mock fit rating
            score = 8 if passed_hard_rules else 4
            reason = "Candidate matches primary qualifications." if passed_hard_rules else "Candidate does not satisfy minimum mandatory criteria."
            return {"fit_rating_0_to_10": score, "one_line_reason": reason}

        prompt_tpl = self._read_prompt("fit_rating_prompt.txt")
        rendered = prompt_tpl.replace("{passed_hard_requirements}", str(passed_hard_rules))\
                             .replace("{job_requirements}", requirements_summary)\
                             .replace("{candidate_summary}", profile_summary)

        response_text = self._call_provider(rendered)
        data = extract_and_validate_json(response_text, required_keys=["fit_rating_0_to_10", "one_line_reason"])

        # Safety enforce rule outcome capping
        if not passed_hard_rules and data["fit_rating_0_to_10"] > 5:
            data["fit_rating_0_to_10"] = 5

        return data

    def generate_explanation(self, profile_data: dict, requirements_data: dict, raw_snippets: str) -> Dict[str, Any]:
        """Generates evidence-grounded explanation and citations."""
        if self.provider == "mock" or not self.api_key:
            # Deterministic fallback
            return {
                "explanation": "Candidate evaluated against core technical competencies and experience gates.",
                "evidence_snippets": [raw_snippets[:120]] if raw_snippets else []
            }

        prompt_tpl = self._read_prompt("explanation_prompt.txt")
        rendered = prompt_tpl.replace("{job_requirements}", json.dumps(requirements_data))\
                             .replace("{candidate_profile}", json.dumps(profile_data))\
                             .replace("{resume_snippets}", raw_snippets[:1000])

        response_text = self._call_provider(rendered)
        return extract_and_validate_json(response_text, required_keys=["explanation", "evidence_snippets"])

    def _call_provider(self, prompt: str) -> str:
        """Dispatches prompt to configured provider API."""
        if self.provider == "gemini":
            import requests
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(url, json=payload, timeout=30)
            resp.raise_for_status()
            res_json = resp.json()
            return res_json["candidates"][0]["content"]["parts"][0]["text"]

        elif self.provider in ["groq", "openai"]:
            import requests
            endpoint = "https://api.groq.com/openai/v1/chat/completions" if self.provider == "groq" else "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
            resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")


llm_client = LLMClient()
