# System Architecture: LLM-Based Resume Screening System (P_101)

## 1. Overview
Project P_101 is an explainable, human-in-the-loop resume screening engine designed to screen technical candidate resumes against detailed job descriptions. It addresses the shortcomings of brittle keyword filters and opaque ranking algorithms by implementing a **transparent 4-tier hybrid AI engine**.

---

## 2. Multi-Tier Hybrid AI Engine

```
                             [ Raw Resume (PDF/DOCX/TXT) ]
                                          │
                                          ▼
                             [ Text Extraction & Normalization ]
                                          │
                        ┌─────────────────┴─────────────────┐
                        │ Optional PII Masking              │
                        │ (Names, Gender Markers, Colleges) │
                        └─────────────────┬─────────────────┘
                                          │
                                          ▼
                             [ Structured Resume Parser ]
                             - Skills Taxonomy Match
                             - Experience & Date Extractor
                             - Education & Project Parser
                                          │
                ┌─────────────────────────┴─────────────────────────┐
                ▼                                                   ▼
      [ Tier 1: Rule Layer ]                             [ Tier 2: NLP/ML Layer ]
      - Mandatory skill gates                            - Skills taxonomy overlap
      - Minimum experience filter                        - Semantic cosine similarity
      - Degree / Education check                         - TF-IDF / Embedding match
                │                                                   │
                └─────────────────────────┬─────────────────────────┘
                                          │
                                          ▼
                               [ Tier 3: LLM Layer ]
                               - Ambiguous section resolution
                               - Fit assessment (capped 0-10)
                               - Evidence-grounded rationale
                                          │
                                          ▼
                              [ Tier 4: Fusion Layer ]
       Weighted Formula: (0.3 * Rule) + (0.4 * Semantic) + (0.2 * Exp) + (0.1 * LLM)
                                          │
                                          ▼
                             [ Recruiter Decision UI ]
                             - Ranked shortlist
                             - Evidence citation snippets
                             - Skill gap analysis
                             - Human override & CSV Export
```

---

## 3. Tier Responsibilities

| Layer | Technique | Role in the System | Hard Gate / Cap |
| :--- | :--- | :--- | :--- |
| **Rule Layer** | Deterministic rule filters | Evaluates mandatory skills, minimum years of experience, and degrees. | Pass/fail flag; failure caps total score. |
| **ML / NLP Layer** | Skills taxonomy, TF-IDF, Cosine Similarity | Measures semantic alignment beyond exact keyword matches. | Continuous score $0.0 \dots 1.0$. |
| **LLM Layer** | Structured JSON schema prompts & Rationale writer | Parses messy sections and extracts readable justification from evidence. | Fit rating capped so it cannot override failed hard requirements. |
| **Fusion Layer** | Configurable weighted sum | Blends all scores into a transparent composite score visible component-by-component. | Weights customizable by recruiter. |
| **Fairness Layer** | PII masking engine | Obfuscates candidate name, gender indicators, and college brand during screening. | Guarantees unbiased first-pass evaluation. |

---

## 4. Database Schema (SQLite)

- **`jobs`**: `id`, `title`, `jd_text`, `requirements_json`, `weights_json`, `created_at`
- **`candidates`**: `id`, `job_id`, `display_id`, `masked`, `created_at`
- **`resumes`**: `id`, `candidate_id`, `filename`, `raw_text`
- **`profiles`**: `id`, `candidate_id`, `skills`, `experience_years`, `education`, `projects`, `certifications`, `professional_summary`
- **`scores`**: `id`, `candidate_id`, `job_id`, `rule`, `semantic`, `experience`, `llm_fit`, `total`, `passed_hard_requirements`, `explanation`, `matched_skills`, `missing_skills`, `evidence`

---

## 5. Security, Ethics, and Human-in-the-Loop
1. **Decision Authority**: The AI generates a shortlist and explains the reasoning, but **never makes final hiring rejections**.
2. **Protected Attributes**: No age, gender, race, caste, religion, or disability information is ingested or used in prompts.
3. **Data Privacy**: Raw uploaded resumes are kept in local storage and excluded from Git commits via `.gitignore`.
