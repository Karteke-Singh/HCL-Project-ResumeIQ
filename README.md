# Project P_101: LLM-Based Resume Screening System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An explainable, bias-safe, human-in-the-loop resume screening engine. Built for recruiters to parse technical resumes, extract structured criteria from job descriptions, evaluate candidates via a transparent hybrid formula, and present evidence-grounded shortlists.

**Student:** Rishi Singh  
**Repository:** `p101-resume-screening-llm-rishi-singh`

---

## 1. Problem Statement
Recruiters receive hundreds of resumes per job opening. Manual screening is slow and prone to fatigue; crude keyword filters reject strong candidates with unconventional phrasing; and unstructured reviews can introduce unconscious bias. 

This project implements an **explainable first-pass assistant** that ranks candidates with component-by-component breakdowns, highlighted evidence, and skill-gap views—leaving the ultimate hiring decision to human recruiters.

---

## 2. Hybrid AI Architecture

```text
Upload (PDF/DOCX/TXT) ──> Text Extraction ──> Bias-Safe Masking (Optional)
                                                     │
                                                     ▼
                                         Structured Resume Parser
                                                     │
               ┌─────────────────────────────────────┴─────────────────────────────────────┐
               ▼                                                                           ▼
      [ Tier 1: Rule Layer ]                                                    [ Tier 2: NLP/ML Layer ]
      - Mandatory skill gates                                                   - Skills taxonomy matching
      - Minimum experience filter                                               - TF-IDF / Embedding similarity
               │                                                                           │
               └─────────────────────────────────────┬─────────────────────────────────────┘
                                                     ▼
                                          [ Tier 3: LLM Layer ]
                                          - Ambiguous section extraction
                                          - Evidence-grounded rationale
                                                     │
                                                     ▼
                                         [ Tier 4: Fusion Layer ]
               Final Score = (0.3 * Rule) + (0.4 * Semantic) + (0.2 * Exp) + (0.1 * LLM Fit)
                                                     │
                                                     ▼
                                      [ Recruiter Streamlit UI ]
```

---

## 3. Quick Start & Setup

### 3.1 Clone & Environment Setup
```bash
git clone https://github.com/rishi-singh/p101-resume-screening-llm-rishi-singh.git
cd p101-resume-screening-llm-rishi-singh

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3.2 Configuration
Copy `.env.example` to `.env` and configure your LLM provider credentials:
```bash
cp .env.example .env
```
*(Supports Gemini, Groq, OpenAI, or an offline Mock provider for zero-API-cost local testing)*.

### 3.3 Initialize & Seed Sample Data
Populate the SQLite database with 2 sample Job Descriptions and 15 benchmark resumes:
```bash
python scripts/seed_data.py
```

### 3.4 Run Day 1 Verification Suite
Verify text extraction, regex/taxonomy parsing, and schema generation:
```bash
python scripts/test_day1.py
# or using pytest
pytest backend/tests/
```

### 3.5 Launch Application
```bash
# Launch Streamlit Frontend:
streamlit run frontend/pages/create-job.py

# Launch FastAPI Backend (Optional):
uvicorn backend.app.main:app --reload --port 8000
```

---

## 4. Sample Benchmark Dataset
The dataset in `data/sample/` consists of:
- **2 Job Descriptions**:
  1. `JOB_001_PY_BACKEND`: Junior Python Backend Developer
  2. `JOB_002_DATA_ENG`: Junior Python Data Engineer
- **15 Plain-Text & JSON Resumes** (`C001` - `C015`): Covers direct matches, framework variants (FastAPI vs Django vs Flask), language variants (Java, C#, Flutter), experience boundary tests (0 vs 2 vs 6 years), and non-matching roles.
- **`ground_truth.csv`**: Provisional human benchmark scores ($1 \dots 5$) for evaluating scoring accuracy and Precision@5.

---

## 5. Ethical Safeguards & Limitations
- **No Protected Attributes**: The system excludes gender, age, race, caste, religion, nationality, and photos from all ranking criteria and prompts.
- **Bias-Safe Mode**: Masking engine obfuscates candidate names, personal markers, and universities during screening.
- **Human Authority**: The AI generates structured explanations and candidate comparisons, but **never automatically sends rejections**.
- **Synthetic Ground Truth**: The sample dataset serves functional pipeline testing and does not constitute production recruitment guarantees.
