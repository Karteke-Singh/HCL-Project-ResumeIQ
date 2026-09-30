# Evaluation Report: LLM-Based Resume Screening System (P_101)

## 1. Evaluation Methodology
To assess the hybrid resume screening engine, we benchmark the model's computed rankings against a verified human-labeled ground truth dataset (`data/sample/ground_truth.csv`) containing 15 candidates across two target roles:
1. **Job 1**: Junior Python Backend Developer (`JOB_001_PY_BACKEND`)
2. **Job 2**: Junior Python Data Engineer (`JOB_002_DATA_ENG`)

---

## 2. Key Metrics
- **Precision@K (P@K)**: Proportion of the top-$K$ model-recommended candidates that belong to human-rated top candidates ($score \ge 4$).
- **Mean Reciprocal Rank (MRR)**: Evaluates whether the best candidate (C001 for Job 1, C006 for Job 2) is positioned at rank #1.
- **Spearman Rank Correlation**: Correlation between automated composite score and ground-truth human ratings (scale 1 to 5).
- **Rule Gate Accuracy**: Accuracy of binary pass/fail enforcement on hard gates (such as minimum experience $\ge 1.0$ year).

---

## 3. Benchmark Ground Truth Reference (Job 1)

| Candidate ID | Human Rating (1-5) | Expected Tier | Key Rationale |
| :---: | :---: | :--- | :--- |
| **C001** | **5** | Top Shortlist | Meets all core skills (Python, FastAPI, SQL, REST, Pytest) with 2 yrs exp. |
| **C002** | **4** | High Consideration | Strong Python & SQL backend with 2 yrs exp; uses Django instead of FastAPI. |
| **C009** | **4** | High Consideration | Highly qualified (6 yrs exp, FastAPI, PostgreSQL), but slightly overqualified for junior role. |
| **C004** | **3** | Borderline / Project | Direct FastAPI projects, but 0 yrs formal experience (minimum experience test). |
| **C007** | **3** | Moderate | 1.5 yrs Python, Flask, SQL, REST APIs (general full-stack). |
| **C013** | **3** | Moderate | 1.5 yrs Python, FastAPI, but MongoDB/NoSQL rather than SQL. |
| **C015** | **3** | Moderate | Python & FastAPI serving, but ML modeling focus. |
| **C003** | **2** | Low | 2 yrs backend with SQL and REST, but in Java/Spring Boot (no Python). |
| **C006** | **2** | Low | 2 yrs Python/SQL, but focused on data pipelines/ETL rather than REST APIs. |
| **C008** | **2** | Low | DevOps / Docker / AWS focus with Python scripting; light on backend APIs. |
| **C010** | **2** | Low | 2 yrs QA API testing with Python/Pytest; lacks core development experience. |
| **C014** | **2** | Low | C#/.NET backend stack; no Python background. |
| **C005** | **1** | Reject / Non-match | Frontend React / CSS / JavaScript; minimal backend relevance. |
| **C011** | **1** | Reject / Non-match | Data Analyst / Power BI / Excel; lacks software engineering. |
| **C012** | **1** | Reject / Non-match | Mobile App Developer (Flutter/Dart); no Python backend. |

---

## 4. Limitations & Ethical Boundary
- **Synthetic Ground Truth**: The benchmark labels represent provisional recruiter judgments for pipeline validation, not immutable truths.
- **Human Oversight**: The system serves as a transparent **first-pass assistant**. Hiring decisions, interview invitations, and rejection notifications must always be confirmed by human recruiters.
- **Fairness Guarantee**: PII masking prevents algorithmic or unconscious bias based on candidate names, gendered terms, and educational institution prestige.
