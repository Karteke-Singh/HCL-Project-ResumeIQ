# Benchmark Dataset: LLM-Based Resume Screening System (Project P_101)

**Student:** Rishi Singh  
**Repository:** `p101-resume-screening-llm-rishi-singh`  
**Target Applications:** Resume Screening, Candidate Ranking, Skill-Gap Analysis, Explainable AI Filtering

---

## 1. Overview & Objective

This benchmark dataset provides a standardized, synthetic test suite designed to evaluate and validate **Project P_101: LLM-Based Resume Screening System**. 

The dataset provides multi-format resumes (**Plain-Text, Microsoft Word DOCX, and PDF**) paired with structured JSON representations, two distinct technical Job Descriptions, and a 30-entry human-evaluated ground-truth matrix for computing ranking precision (e.g., Precision@5, NDCG).

### Key Testing Objectives:
1. **Multi-Format Ingestion:** Verify text extraction across `.txt`, `.docx` (`python-docx`), and `.pdf` (`pdfplumber`).
2. **Entity & Skill Extraction:** Test spaCy NER and skills taxonomy extraction against structured ground truth.
3. **Hard Rule Filtering:** Validate pass/fail gating for minimum experience thresholds (e.g., 1.0 year minimum) and mandatory skill requirements.
4. **Semantic & NLP Similarity:** Measure TF-IDF and embedding cosine similarity on diverse candidate phrasing.
5. **LLM Structured Fallback & Explanation:** Provide realistic candidate contexts for LLM evidence citation without hallucinations.
6. **Fairness & Bias Masking:** Ensure PII masking (names, institutions, emails) operates cleanly without affecting technical evaluation.

---

## 2. Dataset Directory Structure

```text
data/sample/
├── README.md                  # Comprehensive dataset documentation and benchmark calibration guide
├── job_descriptions.json      # 2 target Job Descriptions (Backend Developer & Data Engineer)
├── resumes.json               # 15 structured JSON candidate profiles with schema fields
├── ground_truth.csv           # 30 provisional human relevance labels (1-5 scale) with justifications
└── resumes/
    ├── C001.txt ... C015.txt  # 15 UTF-8 plain-text formatted resumes
    ├── docx/
    │   ├── C001.docx ... C015.docx  # 15 styled Microsoft Word DOCX resumes
    └── pdf/
        ├── C001.pdf ... C015.pdf    # 15 formatted PDF resumes for PDF text extraction testing
```

---

## 3. Schema Reference

### 3.1 Job Descriptions (`job_descriptions.json`)
The file contains an array of job specification objects:

| Field | Type | Description |
| :--- | :--- | :--- |
| `job_id` | String | Unique job identifier (`JOB_001_PY_BACKEND`, `JOB_002_DATA_ENG`). |
| `job_title` | String | Formal role title. |
| `department` | String | Engineering / Analytics department. |
| `location_type` | String | Workplace configuration (Remote, Hybrid, Onsite). |
| `description` | String | Overview of role responsibilities and mission. |
| `minimum_experience_years`| Float | Mandatory baseline professional experience threshold (e.g. `1.0`). |
| `preferred_education` | String | Target academic degree or equivalent practical qualification. |
| `must_have_skills` | Array[String] | Mandatory technical skills scored in the Rule Layer. |
| `nice_to_have_skills` | Array[String] | Preferred technical competencies providing bonus semantic fit. |
| `key_responsibilities` | Array[String] | Key day-to-day duties expected in the role. |

### 3.2 Candidate Profiles (`resumes.json`)
Each candidate object contains structured profile information:

| Field | Type | Description |
| :--- | :--- | :--- |
| `candidate_id` | String | Unique candidate code (`C001` through `C015`). |
| `name` | String | Fictional candidate display label. |
| `professional_summary` | String | Concise summary of technical focus and background. |
| `skills` | Array[String] | Complete list of candidate's technical skills and frameworks. |
| `experience_years` | Float | Verified professional industry experience in years (e.g., `0.0`, `1.5`, `2.0`, `6.0`). |
| `education` | Object | Academic history (`degree`, `field_of_study`, `institution`, `graduation_year`). |
| `work_experience` | Array[Object] | Employment history (`title`, `company`, `duration`, `responsibilities`). |
| `projects` | Array[Object] | Portfolio projects (`name`, `description`, `technologies`). |
| `certifications` | Array[String] | Professional certificates (or empty array `[]`). |

### 3.3 Ground Truth (`ground_truth.csv`)
Columns:
- `job_id`: Target job identifier (`JOB_001_PY_BACKEND` or `JOB_002_DATA_ENG`).
- `candidate_id`: Evaluated candidate identifier (`C001` to `C015`).
- `relevance_1_to_5`: Integer score from 1 (Very Weak Match) to 5 (Very Strong Match).
- `reason`: Grounded human recruiter rationale explaining the score based on skills, experience, and domain alignment.

---

## 4. Benchmark Cohort & Test Scenarios Matrix

The 15 fictional candidates are carefully engineered to represent specific real-world edge cases in technical recruitment:

| ID | Name | Primary Technical Stack | Exp (Yrs) | Role 1 Fit (Backend) | Role 2 Fit (Data Eng) | Test Scenario & Screening Edge Case |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **C001** | Candidate C001 | Python, FastAPI, SQL, PostgreSQL, REST APIs, Git, Pytest | 2.0 | **5 (Direct Match)** | 3 (Moderate) | **Ideal Baseline Match:** Satisfies every hard rule, mandatory skill, and preferred tool for backend API engineering. |
| **C002** | Candidate C002 | Python, Django, SQL, PostgreSQL, REST APIs, Git | 2.0 | **4 (Partial Match)** | 3 (Moderate) | **Framework Transferability:** Strong core Python/SQL; uses Django instead of FastAPI. Tests semantic similarity. |
| **C003** | Candidate C003 | Java, Spring Boot, MySQL, REST APIs, SQL, Git, JUnit | 2.0 | **2 (Weak Match)** | 1 (Very Weak) | **Tech Stack Mismatch:** Professional enterprise backend developer, but in Java instead of Python. Tests language gate. |
| **C004** | Candidate C004 | Python, FastAPI, SQL, REST APIs, Git, Pydantic | 0.0 | **3 (Rule Boundary)** | 2 (Weak) | **Experience Gate Boundary:** High technical skill via academic capstone projects, but 0.0 years professional experience. Tests hard rule filter. |
| **C005** | Candidate C005 | JavaScript, React, HTML5, CSS3, Tailwind CSS, Redux | 2.0 | **1 (Domain Mismatch)**| 1 (Very Weak) | **Domain Mismatch:** Pure frontend UI engineer applying for backend/data roles. Should be filtered to bottom. |
| **C006** | Candidate C006 | Python, SQL, PostgreSQL, ETL, Pandas, Airflow, Docker | 2.0 | **2 (Weak Match)** | **5 (Direct Match)** | **Cross-Role Inversion:** Perfect fit for Data Engineer opening; weak fit for REST API Backend opening. Tests role-specificity. |
| **C007** | Candidate C007 | Python, Flask, SQL, SQLite, JavaScript, HTML5, REST APIs | 1.5 | **3 (Moderate Match)**| 2 (Weak) | **Adjacent Lightweight Stack:** Fullstack web developer using Flask instead of FastAPI and SQLite instead of PostgreSQL. |
| **C008** | Candidate C008 | Linux, Docker, Kubernetes, AWS, Bash, Python, CI/CD | 2.5 | **2 (Weak Match)** | 2 (Weak) | **Infrastructure / DevOps:** Strong cloud, container, and scripting background, but light on backend application code. |
| **C009** | Candidate C009 | Python, FastAPI, Django, PostgreSQL, Redis, Kubernetes | 6.0 | **4 (Overqualified)** | 3 (Moderate) | **Overqualified Senior:** 6 years experience with distributed architecture. Tests whether system handles senior level gracefully. |
| **C010** | Candidate C010 | Python, Pytest, Selenium, REST APIs, CI/CD, Postman | 2.0 | **2 (Weak Match)** | 2 (Weak) | **QA / Automation Engineer:** Knows Python, testing, and APIs, but from a quality assurance perspective rather than feature development. |
| **C011** | Candidate C011 | SQL, Pandas, Tableau, Power BI, Excel, Analytics | 1.5 | **1 (Very Weak)** | **4 (Strong Partial)** | **Analytics to Engineering:** Strong SQL and data manipulation; excels at analytics; partial fit for data engineering. |
| **C012** | Candidate C012 | Flutter, Dart, Firebase, REST APIs, Android, iOS | 2.0 | **1 (Irrelevant)** | 1 (Very Weak) | **Mobile Developer:** Mobile client engineer with zero Python or server infrastructure experience. |
| **C013** | Candidate C013 | Python, FastAPI, MongoDB, REST APIs, Docker | 1.5 | **3 (Moderate Match)**| 2 (Weak) | **Database Paradigm Difference:** Strong Python & FastAPI skills, but relies on NoSQL (MongoDB) instead of relational SQL. |
| **C014** | Candidate C014 | C#, .NET Core, SQL Server, REST APIs, Azure, Git | 1.5 | **2 (Weak Match)** | 1 (Very Weak) | **Compiled Stack Mismatch:** Solid backend REST API and relational SQL skills, but in Microsoft .NET/C# ecosystem. |
| **C015** | Candidate C015 | Python, PyTorch, Scikit-learn, Pandas, FastAPI, ML | 1.5 | **3 (Moderate Match)**| **4 (Strong Partial)** | **Machine Learning Engineer:** Applies Python and FastAPI for model serving; strong Pandas proficiency aligns well with data pipelines. |

---

## 5. Target Job Descriptions Explained

### 5.1 Job 1: Junior Python Backend Developer (`JOB_001_PY_BACKEND`)
- **Department:** Engineering (Microservices team)
- **Minimum Experience:** 1.0 Year
- **Must-Have Skills:** `Python`, `FastAPI`, `SQL`, `REST APIs`, `Git`
- **Nice-to-Have Skills:** `Automated Testing (Pytest)`, `PostgreSQL`, `Docker`, `CI/CD`
- **Benchmark Top Picks:** C001 (Rating 5), C002 (Rating 4), C009 (Rating 4)

### 5.2 Job 2: Junior Python Data Engineer (`JOB_002_DATA_ENG`)
- **Department:** Data & Analytics
- **Minimum Experience:** 1.0 Year
- **Must-Have Skills:** `Python`, `SQL`, `ETL`, `Pandas`, `Git`
- **Nice-to-Have Skills:** `PostgreSQL`, `Apache Airflow`, `Docker`, `Data Modeling`
- **Benchmark Top Picks:** C006 (Rating 5), C011 (Rating 4), C015 (Rating 4)

---

## 6. Synthetic Data Integrity & Ethical Safeguards

1. **Entirely Synthetic Records:**
   - Every candidate name, educational institution, corporate employer, and contact identifier is synthetic.
   - Contact emails utilize the RFC-compliant dummy domain `@synthetic-dataset.local`.
2. **Exclusion of Protected Attributes:**
   - The dataset strictly avoids protected attributes: gender, age, date of birth, marital status, race, ethnicity, religion, caste, nationality, physical address, and photos.
   - Ground truth scores are strictly grounded in demonstrable technical proficiencies, framework mastery, database experience, and verifiable years of practice.
3. **Research & Evaluation Purpose:**
   - This dataset is calibrated for algorithmic verification, pipeline integration, and test automation.
   - It should not be used as training data for neural models claiming legal compliance in employment without domain human calibration.

---

## 7. Reviewer Calibration Guide Prior to Evaluation

When computing ranking accuracy metrics (such as Precision@5, Spearman rank correlation, or NDCG@5), evaluators should review the following calibration nuances:

1. **Experience Gating Policy:**
   - Candidate **C004** demonstrates high competence with Python and FastAPI but has 0.0 professional years. Under a strict hard-gate policy, C004 receives a 0 or 1 on rules. Under a potential-oriented policy, C004 is scored higher based on project quality.
2. **Framework Specificity vs Language Fluency:**
   - Candidate **C002** (Django) vs **C001** (FastAPI): In teams using pure microservices, FastAPI may be mandatory. In teams building general web backends, Django experience is highly transferable.
3. **Seniority Penalty / Capping:**
   - Candidate **C009** has 6 years experience for a junior role. While technically capable (Rating 4), some organizations may flag flight risk or salary mismatch.

---

## 8. Automated Dataset Validation

Run the automated verification script to confirm schema compliance, unique IDs, file presence, and parser readability:

```bash
python scripts/validate_dataset.py
```
