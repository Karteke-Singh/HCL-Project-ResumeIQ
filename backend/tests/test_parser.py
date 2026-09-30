import pytest
from pathlib import Path
from backend.app.services.text_extractor import extract_text_from_file
from backend.app.services.resume_parser import resume_parser_v1
from backend.app.schemas import ParsedProfile

SAMPLE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "sample" / "resumes"


def test_sample_resumes_directory_exists():
    assert SAMPLE_DIR.exists()
    files = list(SAMPLE_DIR.glob("*.txt"))
    assert len(files) == 15


@pytest.mark.parametrize("cid", [f"C{i:03d}" for i in range(1, 16)])
def test_parse_sample_resume(cid):
    file_path = SAMPLE_DIR / f"{cid}.txt"
    assert file_path.exists()

    raw_text = extract_text_from_file(file_path)
    assert len(raw_text) > 100

    profile = resume_parser_v1.parse(raw_text)
    assert isinstance(profile, ParsedProfile)
    assert profile.candidate_id == cid
    assert len(profile.skills) > 0
    assert profile.experience_years >= 0.0

    # Specific profile checks
    if cid == "C001":
        assert "Python" in profile.skills
        assert "FastAPI" in profile.skills
        assert profile.experience_years == 2.0
    elif cid == "C003":
        assert "Java" in profile.skills
        assert "Spring Boot" in profile.skills
    elif cid == "C004":
        assert profile.experience_years == 0.0
        assert "FastAPI" in profile.skills
    elif cid == "C005":
        assert "React" in profile.skills
        assert "JavaScript" in profile.skills
