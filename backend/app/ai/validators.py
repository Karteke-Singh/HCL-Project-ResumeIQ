import json
import re
from typing import Dict, Any, Optional


def extract_and_validate_json(raw_text: str, required_keys: Optional[list] = None) -> Dict[str, Any]:
    """
    Extracts JSON from an LLM response string (stripping markdown code fences if present)
    and verifies that required keys are present.
    """
    cleaned = raw_text.strip()

    # Strip markdown fences ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if match:
        cleaned = match.group(1).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find { ... } block
        obj_match = re.search(r"\{[\s\S]*\}", cleaned)
        if obj_match:
            data = json.loads(obj_match.group(0))
        else:
            raise ValueError(f"Could not parse valid JSON from text: {raw_text[:100]}...")

    if required_keys:
        missing = [k for k in required_keys if k not in data]
        if missing:
            raise ValueError(f"JSON response is missing required keys: {missing}")

    return data
