"""
Day 1 Verification Script.
Tests:
1. Resumes directory contains 15 plain-text resume files.
2. Text extraction works for sample files.
3. Resume parser v1 extracts structured profile JSON.
4. Database initialization and seeding works cleanly.
"""

import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.services.text_extractor import extract_text_from_file
from backend.app.services.resume_parser import resume_parser_v1
from backend.app.schemas import ParsedProfile
from scripts.seed_data import seed
from backend.app.db.session import SessionLocal
from backend.app.db.models import Job, Candidate, Profile, Resume

def main():
    print("=" * 70)
    print("Day 1 Verification: Skeleton, DB Models, 15 Resumes, Parser v1")
    print("=" * 70)

    sample_dir = BASE_DIR / "data" / "sample" / "resumes"
    txt_files = sorted(list(sample_dir.glob("*.txt")))

    print(f"[TEST 1] Checking sample resume files... Found {len(txt_files)}")
    if len(txt_files) != 15:
        print(f"[FAIL] Expected 15 files, found {len(txt_files)}")
        return 1
    print("[PASS] Exactly 15 sample resume text files exist.")

    print("\n[TEST 2] Parsing all 15 resumes with ResumeParserV1...")
    for f in txt_files:
        raw_text = extract_text_from_file(f)
        profile = resume_parser_v1.parse(raw_text)
        assert isinstance(profile, ParsedProfile), f"Profile not ParsedProfile for {f.name}"
        assert profile.candidate_id == f.stem, f"Candidate ID mismatch: {profile.candidate_id} vs {f.stem}"
        print(f"  - Parsed {profile.candidate_id}: {len(profile.skills)} skills, {profile.experience_years} yrs exp, Edu: {profile.education.degree if profile.education else 'N/A'}")

    print("[PASS] All 15 resumes successfully parsed into structured JSON schemas.")

    print("\n[TEST 3] Testing Database Seeding & Models...")
    seed()
    db = SessionLocal()
    try:
        job_count = db.query(Job).count()
        candidate_count = db.query(Candidate).count()
        resume_count = db.query(Resume).count()
        profile_count = db.query(Profile).count()

        print(f"  - Jobs in DB: {job_count}")
        print(f"  - Candidates in DB: {candidate_count}")
        print(f"  - Resumes in DB: {resume_count}")
        print(f"  - Profiles in DB: {profile_count}")

        assert job_count >= 2, "Expected at least 2 jobs in DB"
        assert candidate_count >= 15, "Expected at least 15 candidates in DB"
        print("[PASS] Database models and seed pipeline verified.")
    finally:
        db.close()

    print("\n" + "=" * 70)
    print("[SUCCESS] Day 1 Checkpoint Met: Resumes become structured JSON.")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
