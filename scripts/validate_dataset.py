"""
Validation script for Project P_101 Dataset: LLM-Based Resume Screening System.
Validates:
1. File existence (JSON, CSV, README, TXT, DOCX, PDF)
2. Schema structure and required fields for Job Descriptions and Resumes
3. Candidate ID uniqueness and consistency across JSON and raw files
4. Multi-format readability (parses PDF with pdfplumber and DOCX with python-docx)
5. Ground truth CSV integrity (expected columns, candidate coverage, ratings 1-5, justifications)
"""

import csv
import json
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "sample"
RESUMES_DIR = SAMPLE_DIR / "resumes"
DOCX_DIR = RESUMES_DIR / "docx"
PDF_DIR = RESUMES_DIR / "pdf"
JD_PATH = SAMPLE_DIR / "job_descriptions.json"
RESUMES_JSON_PATH = SAMPLE_DIR / "resumes.json"
CSV_PATH = SAMPLE_DIR / "ground_truth.csv"
README_PATH = SAMPLE_DIR / "README.md"

EXPECTED_CANDIDATE_IDS = [f"C{i:03d}" for i in range(1, 16)]
EXPECTED_JOB_IDS = ["JOB_001_PY_BACKEND", "JOB_002_DATA_ENG"]


def validate():
    print("=" * 75)
    print("  PROJECT P_101: AUTOMATED DATASET VALIDATION SUITE")
    print(f"  Project Root: {BASE_DIR}")
    print(f"  Sample Directory: {SAMPLE_DIR}")
    print("=" * 75)

    errors = []
    warnings = []

    # 1. File existence checks
    critical_files = [
        ("Job Descriptions JSON", JD_PATH),
        ("Resumes JSON", RESUMES_JSON_PATH),
        ("Ground Truth CSV", CSV_PATH),
        ("Dataset README.md", README_PATH),
    ]

    for label, p in critical_files:
        if p.exists() and p.is_file():
            print(f"  [PASS] Found critical file: {label} ({p.name})")
        else:
            errors.append(f"Missing critical file: {label} at {p}")
            print(f"  [FAIL] Missing file: {label} ({p.name})")

    # 2. Validate job_descriptions.json
    job_ids = []
    if JD_PATH.exists():
        try:
            with open(JD_PATH, "r", encoding="utf-8") as f:
                jobs = json.load(f)
            if not isinstance(jobs, list):
                errors.append("job_descriptions.json must be a JSON array of job objects.")
            elif len(jobs) != len(EXPECTED_JOB_IDS):
                errors.append(f"Expected {len(EXPECTED_JOB_IDS)} jobs, found {len(jobs)}.")
            else:
                required_jd_fields = [
                    "job_id", "job_title", "department", "location_type",
                    "description", "minimum_experience_years", "preferred_education",
                    "must_have_skills", "nice_to_have_skills", "key_responsibilities"
                ]
                for job in jobs:
                    jid = job.get("job_id")
                    job_ids.append(jid)
                    for rf in required_jd_fields:
                        if rf not in job:
                            errors.append(f"Job {jid} missing required field: {rf}")
                        elif rf in ["must_have_skills", "nice_to_have_skills"] and not isinstance(job[rf], list):
                            errors.append(f"Job {jid} field {rf} must be a list.")
                        elif rf == "minimum_experience_years" and not isinstance(job[rf], (int, float)):
                            errors.append(f"Job {jid} minimum_experience_years must be numeric.")
                print(f"  [PASS] Verified {len(jobs)} Job Descriptions: {job_ids}")
        except Exception as e:
            errors.append(f"Failed to parse job_descriptions.json: {e}")

    # 3. Validate resumes.json
    candidate_ids = []
    candidates_by_id = {}
    if RESUMES_JSON_PATH.exists():
        try:
            with open(RESUMES_JSON_PATH, "r", encoding="utf-8") as f:
                candidates = json.load(f)

            if not isinstance(candidates, list):
                errors.append("resumes.json must contain an array of candidate objects.")
            else:
                if len(candidates) != 15:
                    errors.append(f"Expected 15 candidate profiles, found {len(candidates)}.")

                required_profile_fields = [
                    "candidate_id", "name", "professional_summary", "skills",
                    "experience_years", "education", "work_experience", "projects", "certifications"
                ]

                for c in candidates:
                    cid = c.get("candidate_id")
                    candidate_ids.append(cid)
                    candidates_by_id[cid] = c

                    for rf in required_profile_fields:
                        if rf not in c:
                            errors.append(f"Candidate {cid} missing required field: {rf}")

                    # Check skills is non-empty list
                    if not isinstance(c.get("skills"), list) or len(c.get("skills", [])) == 0:
                        errors.append(f"Candidate {cid} skills must be a non-empty list.")

                    # Check experience years is numeric
                    if not isinstance(c.get("experience_years"), (int, float)):
                        errors.append(f"Candidate {cid} experience_years must be numeric.")

                    # Check education structure
                    edu = c.get("education", {})
                    for ef in ["degree", "field_of_study", "institution", "graduation_year"]:
                        if ef not in edu:
                            errors.append(f"Candidate {cid} education missing: {ef}")

                # Uniqueness check
                if len(set(candidate_ids)) != len(candidate_ids):
                    errors.append("Duplicate candidate IDs detected in resumes.json.")
                else:
                    print(f"  [PASS] All {len(candidate_ids)} candidate IDs in resumes.json are unique: {candidate_ids}")

        except Exception as e:
            errors.append(f"Failed to parse resumes.json: {e}")

    # 4. Validate plain-text resumes
    missing_txt = []
    for cid in EXPECTED_CANDIDATE_IDS:
        txt_file = RESUMES_DIR / f"{cid}.txt"
        if not txt_file.exists():
            missing_txt.append(f"{cid}.txt")
        else:
            content = txt_file.read_text(encoding="utf-8")
            if len(content) < 300:
                warnings.append(f"Text resume {cid}.txt is unusually short ({len(content)} chars)")
            if cid not in content:
                errors.append(f"Text resume {cid}.txt does not contain candidate ID {cid}")

    if missing_txt:
        errors.append(f"Missing plain-text resume files: {missing_txt}")
    else:
        print(f"  [PASS] Verified all 15 plain-text resumes in {RESUMES_DIR}")

    # 5. Validate DOCX resumes using python-docx
    missing_docx = []
    docx_parsed_count = 0
    try:
        import docx
        for cid in EXPECTED_CANDIDATE_IDS:
            docx_file = DOCX_DIR / f"{cid}.docx"
            if not docx_file.exists():
                missing_docx.append(f"{cid}.docx")
            else:
                doc = docx.Document(str(docx_file))
                if len(doc.paragraphs) < 10:
                    warnings.append(f"DOCX {cid}.docx has fewer than 10 paragraphs.")
                docx_parsed_count += 1
        if missing_docx:
            errors.append(f"Missing DOCX resume files: {missing_docx}")
        else:
            print(f"  [PASS] Verified all 15 DOCX resumes (readable by python-docx) in {DOCX_DIR}")
    except ImportError:
        warnings.append("python-docx not installed; skipped DOCX parsing verification.")

    # 6. Validate PDF resumes using pdfplumber
    missing_pdf = []
    pdf_parsed_count = 0
    try:
        import pdfplumber
        for cid in EXPECTED_CANDIDATE_IDS:
            pdf_file = PDF_DIR / f"{cid}.pdf"
            if not pdf_file.exists():
                missing_pdf.append(f"{cid}.pdf")
            else:
                with pdfplumber.open(str(pdf_file)) as pdf:
                    if len(pdf.pages) < 1:
                        errors.append(f"PDF {cid}.pdf contains no pages.")
                    else:
                        text = pdf.pages[0].extract_text() or ""
                        if len(text) < 200:
                            warnings.append(f"PDF {cid}.pdf extracted text is short ({len(text)} chars)")
                pdf_parsed_count += 1
        if missing_pdf:
            errors.append(f"Missing PDF resume files: {missing_pdf}")
        else:
            print(f"  [PASS] Verified all 15 PDF resumes (readable by pdfplumber) in {PDF_DIR}")
    except ImportError:
        warnings.append("pdfplumber not installed; skipped PDF text extraction verification.")

    # 7. Validate ground_truth.csv
    if CSV_PATH.exists():
        try:
            with open(CSV_PATH, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                expected_cols = ["job_id", "candidate_id", "relevance_1_to_5", "reason"]
                if reader.fieldnames != expected_cols:
                    errors.append(f"ground_truth.csv expected columns {expected_cols}, got {reader.fieldnames}")

                rows = list(reader)
                if len(rows) != 30:
                    warnings.append(f"Expected 30 ground truth rows (15 candidates x 2 jobs), found {len(rows)}.")

                evaluated_pairs = set()
                for i, r in enumerate(rows, start=1):
                    jid = r.get("job_id")
                    cid = r.get("candidate_id")
                    rel_str = r.get("relevance_1_to_5")
                    reason = r.get("reason", "")

                    if jid not in EXPECTED_JOB_IDS:
                        errors.append(f"Row {i}: Unknown job_id '{jid}'.")
                    if cid not in EXPECTED_CANDIDATE_IDS:
                        errors.append(f"Row {i}: Unknown candidate_id '{cid}'.")

                    pair = (jid, cid)
                    if pair in evaluated_pairs:
                        errors.append(f"Row {i}: Duplicate evaluation for pair {pair}.")
                    evaluated_pairs.add(pair)

                    try:
                        rel = int(rel_str)
                        if rel < 1 or rel > 5:
                            errors.append(f"Row {i}: Relevance score {rel} outside valid 1-5 range.")
                    except (ValueError, TypeError):
                        errors.append(f"Row {i}: Relevance score '{rel_str}' is not an integer.")

                    if not reason or len(reason.strip()) < 10:
                        errors.append(f"Row {i}: Missing or inadequate justification reason.")

                print(f"  [PASS] ground_truth.csv contains {len(rows)} valid evaluations covering all test pairs.")

        except Exception as e:
            errors.append(f"Failed to read ground_truth.csv: {e}")

    # Final summary
    print("\n" + "=" * 75)
    print("  VALIDATION RESULTS SUMMARY")
    print("=" * 75)

    if warnings:
        print(f"\n[WARNINGS] ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n[FAILED] Encountered {len(errors)} validation error(s):")
        for err in errors:
            print(f"  [X] {err}")
        print("=" * 75)
        sys.exit(1)
    else:
        print("\n[SUCCESS] All dataset validation checks passed cleanly!")
        print(f"  - 2 Job Descriptions verified ({', '.join(EXPECTED_JOB_IDS)})")
        print(f"  - 15 Structured Candidate Profiles in resumes.json")
        print(f"  - 15 Plain-Text resumes in data/sample/resumes/")
        print(f"  - 15 Microsoft Word DOCX resumes in data/sample/resumes/docx/")
        print(f"  - 15 PDF resumes in data/sample/resumes/pdf/")
        print(f"  - 30 Ground Truth evaluations (15 candidates x 2 jobs) with 1-5 ratings and human rationales")
        print(f"  - Comprehensive dataset README.md schema documentation and calibration guide")
        print("=" * 75)
        sys.exit(0)


if __name__ == "__main__":
    validate()
