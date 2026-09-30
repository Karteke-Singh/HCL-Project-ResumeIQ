"""
Seed script to populate SQLite database with sample Jobs and Candidates.
"""

import json
from pathlib import Path
from backend.app.config import settings
from backend.app.db.session import SessionLocal, init_db
from backend.app.db.models import Job, Candidate, Resume, Profile
from backend.app.services.text_extractor import extract_text_from_file
from backend.app.services.resume_parser import resume_parser_v1


def seed():
    print("Initializing Database...")
    init_db()
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Job).count() > 0:
            print("[INFO] Database already contains jobs. Skipping seed.")
            return

        sample_dir = settings.SAMPLE_DATA_DIR
        jd_file = sample_dir / "job_descriptions.json"
        resumes_file = sample_dir / "resumes.json"
        resumes_dir = sample_dir / "resumes"

        with open(jd_file, "r", encoding="utf-8") as f:
            jds = json.load(f)

        created_jobs = {}
        for jd in jds:
            job = Job(
                id=jd["job_id"],
                title=jd["job_title"],
                jd_text=jd["description"],
                requirements_json=json.dumps({
                    "must_have_skills": jd["must_have_skills"],
                    "nice_to_have_skills": jd["nice_to_have_skills"],
                    "minimum_experience_years": jd["minimum_experience_years"],
                    "preferred_education": jd["preferred_education"],
                    "key_responsibilities": jd["key_responsibilities"]
                }),
                weights_json=json.dumps({
                    "rule": settings.WEIGHT_RULE,
                    "semantic": settings.WEIGHT_SEMANTIC,
                    "experience": settings.WEIGHT_EXPERIENCE,
                    "llm_fit": settings.WEIGHT_LLM_FIT
                })
            )
            db.add(job)
            created_jobs[jd["job_id"]] = job

        db.commit()
        print(f"[OK] Seeded {len(created_jobs)} jobs.")

        # Seed candidates under Job 1
        target_job_id = "JOB_001_PY_BACKEND"
        txt_files = sorted(list(resumes_dir.glob("*.txt")))

        for txt_path in txt_files:
            cid = txt_path.stem
            raw_text = extract_text_from_file(txt_path)
            profile_data = resume_parser_v1.parse(raw_text, candidate_id_hint=cid)

            candidate = Candidate(
                job_id=target_job_id,
                display_id=cid,
                masked=False
            )
            db.add(candidate)
            db.flush()

            resume_entry = Resume(
                candidate_id=candidate.id,
                filename=txt_path.name,
                raw_text=raw_text
            )
            db.add(resume_entry)

            profile_entry = Profile(
                candidate_id=candidate.id,
                skills=json.dumps(profile_data.skills),
                experience_years=profile_data.experience_years,
                education=json.dumps(profile_data.education.model_dump() if profile_data.education else {}),
                projects=json.dumps([p.model_dump() for p in profile_data.projects]),
                certifications=json.dumps(profile_data.certifications),
                professional_summary=profile_data.professional_summary
            )
            db.add(profile_entry)

        db.commit()
        print(f"[OK] Seeded {len(txt_files)} candidates with parsed profiles and resumes under {target_job_id}.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
