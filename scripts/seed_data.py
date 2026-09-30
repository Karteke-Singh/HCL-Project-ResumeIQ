"""
Comprehensive Seed Script for Project P_101: LLM-Based Resume Screening System.
Populates SQLite database (resume_screener.db) with:
1. Jobs: 2 realistic Job Descriptions with JSON criteria & weights
2. Candidates: 15 candidate records per job (30 candidate entries total)
3. Resumes: Raw text resumes for each candidate
4. Profiles: Structured skills, experience, education, projects, certifications in JSON
5. Scores: Component breakdowns (rule, semantic, experience, llm_fit, total) and human rationales
"""

import csv
import json
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.config import settings
from backend.app.db.session import SessionLocal, init_db, engine, Base
from backend.app.db.models import Job, Candidate, Resume, Profile, Score


def seed(reset: bool = True):
    print("=" * 70)
    print("  SEEDING SQLITE DATABASE (resume_screener.db)")
    print(f"  Target DB: {settings.DATABASE_URL}")
    print("=" * 70)

    if reset:
        print("[INFO] Resetting tables...")
        Base.metadata.drop_all(bind=engine)

    init_db()
    db = SessionLocal()

    try:
        sample_dir = settings.SAMPLE_DATA_DIR
        jd_file = sample_dir / "job_descriptions.json"
        resumes_file = sample_dir / "resumes.json"
        resumes_dir = sample_dir / "resumes"
        gt_file = sample_dir / "ground_truth.csv"

        # 1. Load data files
        with open(jd_file, "r", encoding="utf-8") as f:
            jds = json.load(f)

        with open(resumes_file, "r", encoding="utf-8") as f:
            candidates_json = json.load(f)

        candidates_map = {c["candidate_id"]: c for c in candidates_json}

        ground_truth_map = {}
        if gt_file.exists():
            with open(gt_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ground_truth_map[(row["job_id"], row["candidate_id"])] = {
                        "relevance": int(row["relevance_1_to_5"]),
                        "reason": row["reason"]
                    }

        # 2. Seed Jobs
        created_jobs = {}
        for jd in jds:
            jid = jd["job_id"]
            job = Job(
                id=jid,
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
            created_jobs[jid] = job

        db.commit()
        print(f"[OK] Seeded {len(created_jobs)} jobs: {list(created_jobs.keys())}")

        # 3. Seed Candidates, Resumes, Profiles, and Scores for each Job
        candidate_count = 0
        resume_count = 0
        profile_count = 0
        score_count = 0

        for jid, job in created_jobs.items():
            reqs = json.loads(job.requirements_json)
            must_have = set(s.lower() for s in reqs["must_have_skills"])
            min_exp = float(reqs["minimum_experience_years"])

            for c_info in candidates_json:
                cid = c_info["candidate_id"]

                # Read raw text resume
                txt_path = resumes_dir / f"{cid}.txt"
                raw_text = txt_path.read_text(encoding="utf-8") if txt_path.exists() else c_info.get("professional_summary", "")

                # Create Candidate
                cand = Candidate(
                    job_id=jid,
                    display_id=cid,
                    masked=False
                )
                db.add(cand)
                db.flush()
                candidate_count += 1

                # Create Resume
                res_entry = Resume(
                    candidate_id=cand.id,
                    filename=f"{cid}.txt",
                    raw_text=raw_text
                )
                db.add(res_entry)
                resume_count += 1

                # Create Profile
                prof_entry = Profile(
                    candidate_id=cand.id,
                    skills=json.dumps(c_info["skills"]),
                    experience_years=c_info["experience_years"],
                    education=json.dumps(c_info.get("education", {})),
                    projects=json.dumps(c_info.get("projects", [])),
                    certifications=json.dumps(c_info.get("certifications", [])),
                    professional_summary=c_info.get("professional_summary", "")
                )
                db.add(prof_entry)
                profile_count += 1

                # Calculate Scores from Ground Truth & Rules
                c_skills = set(s.lower() for s in c_info["skills"])
                matched = [s for s in reqs["must_have_skills"] if s.lower() in c_skills]
                missing = [s for s in reqs["must_have_skills"] if s.lower() not in c_skills]

                exp_years = float(c_info.get("experience_years", 0.0))
                passed_exp = exp_years >= min_exp
                skill_ratio = len(matched) / len(must_have) if must_have else 1.0
                passed_hard = passed_exp and (skill_ratio >= 0.5)

                rule_score = round(0.6 * skill_ratio + 0.4 * min(1.0, exp_years / max(min_exp, 1.0)), 2)

                # Ground truth rating (1-5)
                gt = ground_truth_map.get((jid, cid), {"relevance": 3, "reason": "Standard candidate evaluation"})
                relevance = gt["relevance"]
                llm_fit = round(relevance / 5.0, 2)
                semantic_score = round(min(1.0, 0.4 + (skill_ratio * 0.5)), 2)
                experience_score = round(min(1.0, exp_years / max(min_exp, 1.0)), 2)

                # Weighted total
                raw_total = (
                    settings.WEIGHT_RULE * rule_score +
                    settings.WEIGHT_SEMANTIC * semantic_score +
                    settings.WEIGHT_EXPERIENCE * experience_score +
                    settings.WEIGHT_LLM_FIT * llm_fit
                )
                total_score = round(min(raw_total * 100, 55.0) if not passed_hard else raw_total * 100, 1)

                evidence_list = [f"Direct experience with {skill} documented in work history" for skill in matched[:3]]

                score_entry = Score(
                    candidate_id=cand.id,
                    job_id=jid,
                    rule=rule_score,
                    semantic=semantic_score,
                    experience=experience_score,
                    llm_fit=llm_fit,
                    total=total_score,
                    passed_hard_requirements=passed_hard,
                    explanation=gt["reason"],
                    matched_skills=json.dumps(matched),
                    missing_skills=json.dumps(missing),
                    evidence=json.dumps(evidence_list)
                )
                db.add(score_entry)
                score_count += 1

        db.commit()
        print(f"[OK] Seeded {candidate_count} candidate records.")
        print(f"[OK] Seeded {resume_count} resume records.")
        print(f"[OK] Seeded {profile_count} profile records.")
        print(f"[OK] Seeded {score_count} score evaluation records.")

        # Verify DB file on disk
        db_file = PROJECT_ROOT / "resume_screener.db"
        if db_file.exists():
            print(f"\n[SUCCESS] SQLite database successfully generated: {db_file} ({db_file.stat().st_size} bytes)")
        else:
            print(f"\n[INFO] Database created at {settings.DATABASE_URL}")

    finally:
        db.close()


if __name__ == "__main__":
    seed(reset=True)
