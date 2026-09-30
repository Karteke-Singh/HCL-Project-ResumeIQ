# Recruiter Demo Script: LLM-Based Resume Screening System (P_101)

## Demo Goal
Demonstrate an end-to-end resume screening workflow for 15 resumes against a Junior Python Backend Developer job in under 2 minutes, showcasing transparent scoring, evidence highlights, bias-safe masking, and CSV export.

---

## Step 1: Job Creation & Requirement Extraction
1. Open the Streamlit application: `streamlit run frontend/pages/create-job.py`.
2. Select or paste the **Junior Python Backend Developer** job description.
3. Click **"Extract Requirements"**:
   - Point out automatic classification of **Must-Have** skills (`Python`, `FastAPI`, `SQL`, `REST APIs`, `Git`).
   - Point out **Nice-to-Have** skills (`Pytest`, `PostgreSQL`, `Docker`, `CI/CD`).
   - Observe minimum experience threshold set to `1.0` year.
4. Save the job.

---

## Step 2: Bulk Resume Upload & Parsing
1. Navigate to **"Upload Resumes"** page.
2. Select the sample resumes from `data/sample/resumes/` (or drag-and-drop PDF/DOCX/TXT files).
3. Click **"Process & Parse Resumes"**:
   - The system extracts text using `pdfplumber` / `python-docx`.
   - The rule/NLP parser maps candidate text into structured JSON profiles (skills, experience years, education, projects).

---

## Step 3: Bias-Safe Screening & Hybrid Scoring
1. Navigate to **"Rankings"** page.
2. Toggle **"Bias-Safe Mode"**:
   - Show how candidate names, genders, and university names are masked to prevent unconscious recruiter bias.
3. Click **"Run Hybrid Screening Pipeline"**:
   - **Rule Layer**: Checks 1-year minimum experience and must-have skills.
   - **Semantic Layer**: Computes embedding and taxonomy similarity.
   - **LLM Layer**: Validates ambiguous sections and generates evidence citations.
   - **Fusion Layer**: Blends scores according to configurable weights (`0.3` Rule, `0.4` Semantic, `0.2` Exp, `0.1` LLM).

---

## Step 4: Candidate Detail & Skill-Gap Analysis
1. Select candidate **C001** (Top rank, Score: ~95%):
   - Review matched skills (`Python`, `FastAPI`, `SQL`, `Pytest`).
   - Review evidence snippet quoted directly from the resume text.
2. Select candidate **C004** (Entry-level project developer):
   - Notice the rule failure flag: fails 1-year minimum professional experience gate.
   - Observe that the hybrid formula penalizes the score proportionally without discarding their project work entirely.
3. Select candidate **C005** (Frontend developer):
   - Review skill gap view showing missing `FastAPI`, `SQL`, and backend experience.

---

## Step 5: Side-by-Side Comparison & CSV Export
1. Navigate to **"Compare Candidates"** page and compare **C001** vs **C002**.
2. Click **"Export Shortlist to CSV"**:
   - Download the clean CSV report with candidate IDs, scores, breakdown, and notes for hiring manager review.
