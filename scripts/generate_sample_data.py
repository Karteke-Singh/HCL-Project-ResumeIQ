"""
Sample Dataset Generator for Project P_101.
Generates:
1. data/sample/resumes.json (15 structured candidate profiles)
2. data/sample/resumes/C001.txt to C015.txt (consistent readable plain-text resumes)
3. data/sample/ground_truth.csv (relevance ratings for Job 1 and Job 2)
"""

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DIR = BASE_DIR / "data" / "sample"
RESUMES_DIR = SAMPLE_DIR / "resumes"
RESUMES_DIR.mkdir(parents=True, exist_ok=True)

CANDIDATES = [
    {
        "candidate_id": "C001",
        "name": "Candidate C001",
        "professional_summary": "Junior Backend Developer with 2 years of experience building scalable RESTful APIs and microservices using Python, FastAPI, and PostgreSQL. Experienced in SQL database design, Git version control, and writing automated tests with Pytest.",
        "skills": ["Python", "FastAPI", "SQL", "PostgreSQL", "REST APIs", "Git", "Pytest", "Automated Testing", "Docker"],
        "experience_years": 2.0,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Computer Science", "institution": "Apex University", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior Backend Developer",
                "company": "Nexus Web Services",
                "duration": "2024 - Present (2 years)",
                "responsibilities": [
                    "Developed asynchronous RESTful endpoints using Python and FastAPI.",
                    "Designed PostgreSQL database schemas and optimized SQL queries.",
                    "Wrote unit and integration tests using Pytest with 85%+ coverage.",
                    "Maintained code repository using Git and participated in peer reviews."
                ]
            }
        ],
        "projects": [
            {
                "name": "E-Commerce Checkout Service",
                "description": "Asynchronous microservice managing order flow, payments, and inventory status.",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "Pytest"]
            }
        ],
        "certifications": ["Certified Entry-Level Python Programmer (PCEP)"]
    },
    {
        "candidate_id": "C002",
        "name": "Candidate C002",
        "professional_summary": "Backend Developer with 2 years of experience developing web applications using Python and Django. Skilled in REST API design, relational SQL databases, and database schema migrations.",
        "skills": ["Python", "Django", "Django REST Framework", "SQL", "PostgreSQL", "REST APIs", "Git", "Relational Database Design"],
        "experience_years": 2.0,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Information Technology", "institution": "Crestview Institute of Technology", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior Software Developer",
                "company": "Beacon Digital Solutions",
                "duration": "2024 - Present (2 years)",
                "responsibilities": [
                    "Built web services and REST endpoints using Django and Python.",
                    "Managed PostgreSQL database schemas and performed data migrations using SQL.",
                    "Collaborated with frontend teams via Git."
                ]
            }
        ],
        "projects": [
            {
                "name": "Customer Support CRM",
                "description": "Ticketing and support portal API with relational PostgreSQL storage.",
                "technologies": ["Python", "Django", "PostgreSQL", "Git"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C003",
        "name": "Candidate C003",
        "professional_summary": "Junior Backend Software Engineer with 2 years of enterprise experience building robust backend microservices using Java and Spring Boot. Strong grasp of relational databases with MySQL, RESTful API architecture, and CI/CD pipelines.",
        "skills": ["Java", "Spring Boot", "MySQL", "REST APIs", "SQL", "Git", "Maven", "JUnit", "CI/CD"],
        "experience_years": 2.0,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Software Engineering", "institution": "Highland Engineering College", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior Java Backend Developer",
                "company": "Sterling Enterprise Systems",
                "duration": "2024 - Present (2 years)",
                "responsibilities": [
                    "Engineered enterprise REST APIs using Java 17 and Spring Boot.",
                    "Wrote complex MySQL queries and stored procedures.",
                    "Authored automated unit tests with JUnit."
                ]
            }
        ],
        "projects": [
            {
                "name": "Banking Transaction Gateway",
                "description": "High-volume transaction ledger with relational database persistence.",
                "technologies": ["Java", "Spring Boot", "MySQL", "Git"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C004",
        "name": "Candidate C004",
        "professional_summary": "Recent Computer Science graduate with hands-on academic and open-source project experience designing backend systems with Python, FastAPI, and SQL. Built multiple asynchronous REST APIs during capstone coursework. Seeking first professional software engineering role.",
        "skills": ["Python", "FastAPI", "SQL", "SQLite", "PostgreSQL", "REST APIs", "Git", "Pydantic", "Pytest"],
        "experience_years": 0.0,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Computer Science", "institution": "Metro State University", "graduation_year": 2026},
        "work_experience": [],
        "projects": [
            {
                "name": "Smart Campus Event API",
                "description": "Asynchronous backend API built using FastAPI, Pydantic schemas, and SQL database models.",
                "technologies": ["Python", "FastAPI", "SQL", "SQLite", "Git"]
            },
            {
                "name": "Personal Expense Tracker API",
                "description": "RESTful service providing CRUD operations for budget tracking with JWT authentication.",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "Pytest"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C005",
        "name": "Candidate C005",
        "professional_summary": "Frontend Developer with 2 years of professional experience specializing in client-side web development using modern JavaScript, React, HTML5, and CSS3/Tailwind CSS. Skilled in creating responsive, accessible UI components.",
        "skills": ["JavaScript", "React", "HTML5", "CSS3", "Tailwind CSS", "Redux", "Webpack", "Git", "REST API Integration"],
        "experience_years": 2.0,
        "education": {"degree": "Bachelor of Arts", "field_of_study": "Digital Media and Web Design", "institution": "Summit Art and Tech College", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Frontend Developer",
                "company": "PixelCraft Studios",
                "duration": "2024 - Present (2 years)",
                "responsibilities": [
                    "Built responsive, interactive user interfaces for SaaS dashboards using React and Tailwind CSS.",
                    "Connected user interfaces to backend REST APIs and handled frontend data validation.",
                    "Maintained component libraries and tracked code changes using Git."
                ]
            }
        ],
        "projects": [
            {
                "name": "Analytics Dashboard UI",
                "description": "Interactive data visualization dashboard with dark mode and charting components.",
                "technologies": ["React", "JavaScript", "Tailwind CSS"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C006",
        "name": "Candidate C006",
        "professional_summary": "Junior Data Engineer with 2 years of experience designing data pipelines, ETL workflows, and relational database warehouses using Python, SQL, and PostgreSQL. Proficient with Pandas and Apache Airflow.",
        "skills": ["Python", "SQL", "PostgreSQL", "ETL", "Pandas", "Apache Airflow", "Git", "Data Modeling", "Docker"],
        "experience_years": 2.0,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Data Science", "institution": "Pacific Tech University", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior Data Engineer",
                "company": "DataStream Analytics",
                "duration": "2024 - Present (2 years)",
                "responsibilities": [
                    "Built automated ETL pipelines extracting business data using Python and Pandas.",
                    "Designed and maintained PostgreSQL data warehouse schemas using SQL.",
                    "Scheduled workflow DAGs in Apache Airflow."
                ]
            }
        ],
        "projects": [
            {
                "name": "Automated Financial ETL Pipeline",
                "description": "Daily pipeline transforming high-volume transaction records into analytics tables.",
                "technologies": ["Python", "SQL", "Pandas", "PostgreSQL", "Airflow"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C007",
        "name": "Candidate C007",
        "professional_summary": "Junior Full-Stack / Python Developer with 1.5 years of experience building web applications using Python, Flask, SQL, and JavaScript. Comfortable working across both lightweight backend APIs and client-side interfaces.",
        "skills": ["Python", "Flask", "SQL", "SQLite", "JavaScript", "HTML5", "CSS3", "REST APIs", "Git"],
        "experience_years": 1.5,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Computer Science", "institution": "Valley State University", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior Full Stack Developer",
                "company": "OmniApp Solutions",
                "duration": "2024 - Present (1.5 years)",
                "responsibilities": [
                    "Developed backend API services using Flask and Python.",
                    "Created database tables and queries using SQL.",
                    "Built lightweight frontend interfaces using JavaScript and HTML."
                ]
            }
        ],
        "projects": [
            {
                "name": "Inventory Tracking Web App",
                "description": "Web portal for tracking warehouse stock levels with Flask backend and SQLite database.",
                "technologies": ["Python", "Flask", "SQL", "JavaScript"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C008",
        "name": "Candidate C008",
        "professional_summary": "Cloud and DevOps Engineer with 2.5 years of experience managing Linux infrastructure, Docker containerization, Kubernetes clusters, and CI/CD pipelines. Uses Python and Bash for operations automation.",
        "skills": ["Linux", "Docker", "Kubernetes", "AWS", "Bash", "Python", "CI/CD", "Git", "Terraform"],
        "experience_years": 2.5,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Network Systems", "institution": "Northwest Polytechnic", "graduation_year": 2023},
        "work_experience": [
            {
                "title": "Associate DevOps Engineer",
                "company": "CloudForge Infrastructure",
                "duration": "2023 - Present (2.5 years)",
                "responsibilities": [
                    "Managed Docker container deployments and Kubernetes clusters.",
                    "Automated infrastructure provisioning and monitoring using Python and Bash scripts.",
                    "Constructed CI/CD deployment pipelines using GitHub Actions."
                ]
            }
        ],
        "projects": [
            {
                "name": "Automated Cloud Deployment Runner",
                "description": "Python CLI tool for provisioning AWS instances and Dockerized environments.",
                "technologies": ["Python", "Docker", "AWS", "Bash"]
            }
        ],
        "certifications": ["AWS Certified Cloud Practitioner"]
    },
    {
        "candidate_id": "C009",
        "name": "Candidate C009",
        "professional_summary": "Senior Backend Software Engineer with 6 years of industry experience architecting distributed backend services with Python, FastAPI, Django, and PostgreSQL. Experienced in distributed caching, Kubernetes, and mentoring junior engineers.",
        "skills": ["Python", "FastAPI", "Django", "SQL", "PostgreSQL", "Redis", "Docker", "Kubernetes", "REST APIs", "Git", "CI/CD", "Microservices"],
        "experience_years": 6.0,
        "education": {"degree": "Master of Science", "field_of_study": "Computer Science", "institution": "National Institute of Science", "graduation_year": 2020},
        "work_experience": [
            {
                "title": "Senior Backend Engineer",
                "company": "Horizon Cloud Systems",
                "duration": "2022 - Present (4 years)",
                "responsibilities": [
                    "Architected high-throughput microservices using Python and FastAPI.",
                    "Optimized PostgreSQL queries, indexing, and connection pools.",
                    "Guided architecture decisions and mentored junior developers."
                ]
            },
            {
                "title": "Software Engineer",
                "company": "TerraTech Labs",
                "duration": "2020 - 2022 (2 years)",
                "responsibilities": [
                    "Developed backend web APIs using Django and PostgreSQL.",
                    "Built automated testing pipelines with Pytest and Docker."
                ]
            }
        ],
        "projects": [
            {
                "name": "Distributed Event Engine",
                "description": "Enterprise event streaming and API gateway processing millions of messages daily.",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"]
            }
        ],
        "certifications": ["AWS Certified Solutions Architect"]
    },
    {
        "candidate_id": "C010",
        "name": "Candidate C010",
        "professional_summary": "QA Automation Engineer with 2 years of experience writing automated test suites for REST APIs and web applications using Python, Pytest, and Selenium. Proficient in database query verification with SQL.",
        "skills": ["Python", "Pytest", "Selenium", "Automated Testing", "REST APIs", "SQL", "PostgreSQL", "Git", "CI/CD"],
        "experience_years": 2.0,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Computer Science", "institution": "Coastline University", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "QA Automation Engineer",
                "company": "QualityFirst Tech",
                "duration": "2024 - Present (2 years)",
                "responsibilities": [
                    "Developed comprehensive end-to-end API testing frameworks using Python and Pytest.",
                    "Executed automated SQL queries to validate database state and data integrity.",
                    "Integrated automated test runs into CI/CD build pipelines."
                ]
            }
        ],
        "projects": [
            {
                "name": "API Regression Testing Suite",
                "description": "Automated regression framework validating over 200 backend REST endpoints.",
                "technologies": ["Python", "Pytest", "REST APIs", "Git"]
            }
        ],
        "certifications": ["ISTQB Certified Tester"]
    },
    {
        "candidate_id": "C011",
        "name": "Candidate C011",
        "professional_summary": "Data Analyst with 1.5 years of experience delivering quantitative reports, dashboards, and SQL analytics. Skilled with Power BI, Excel, Tableau, and data manipulation in Python with Pandas.",
        "skills": ["SQL", "Python", "Pandas", "Power BI", "Tableau", "Excel", "Data Analysis", "Git"],
        "experience_years": 1.5,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Business Analytics", "institution": "Midwest Business School", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior Data Analyst",
                "company": "Insights Corp",
                "duration": "2024 - Present (1.5 years)",
                "responsibilities": [
                    "Wrote complex SQL queries to extract KPIs for executive leadership.",
                    "Created interactive reporting dashboards using Power BI and Tableau.",
                    "Preprocessed raw data tables using Python and Pandas."
                ]
            }
        ],
        "projects": [
            {
                "name": "Customer Churn Analytics Dashboard",
                "description": "Interactive Power BI dashboard tracking monthly cohort retention metrics.",
                "technologies": ["SQL", "Power BI", "Python", "Pandas"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C012",
        "name": "Candidate C012",
        "professional_summary": "Mobile Application Developer with 2 years of experience crafting cross-platform iOS and Android apps using Flutter and Dart. Strong knowledge of REST API consumption, Firebase backend services, and Git.",
        "skills": ["Flutter", "Dart", "Firebase", "Android", "iOS", "REST APIs", "Git", "Mobile Development"],
        "experience_years": 2.0,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Software Engineering", "institution": "Southern Tech University", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior Mobile Developer",
                "company": "AppNova Studios",
                "duration": "2024 - Present (2 years)",
                "responsibilities": [
                    "Built cross-platform mobile user interfaces using Flutter and Dart.",
                    "Integrated client applications with backend REST APIs and Firebase auth.",
                    "Managed mobile build releases and Git versioning."
                ]
            }
        ],
        "projects": [
            {
                "name": "Fitness Habit Tracker App",
                "description": "Cross-platform mobile app tracking daily workouts and nutritional goals.",
                "technologies": ["Flutter", "Dart", "Firebase", "REST APIs"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C013",
        "name": "Candidate C013",
        "professional_summary": "Backend Developer with 1.5 years of experience building modern asynchronous REST APIs using Python and FastAPI, paired primarily with MongoDB and Docker container environments.",
        "skills": ["Python", "FastAPI", "MongoDB", "NoSQL", "REST APIs", "Docker", "Git", "Pydantic"],
        "experience_years": 1.5,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Computer Engineering", "institution": "Granite State Tech", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior Backend Developer",
                "company": "Veloce Technologies",
                "duration": "2024 - Present (1.5 years)",
                "responsibilities": [
                    "Engineered asynchronous backend endpoints in Python using FastAPI.",
                    "Modeled unstructured application collections in MongoDB.",
                    "Containerized microservices using Docker for testing and deployment."
                ]
            }
        ],
        "projects": [
            {
                "name": "Content Management Microservice",
                "description": "FastAPI document storage API backed by MongoDB.",
                "technologies": ["Python", "FastAPI", "MongoDB", "Docker"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C014",
        "name": "Candidate C014",
        "professional_summary": "Backend Developer with 1.5 years of enterprise experience building web APIs and server-side components using C#, ASP.NET Core, and Microsoft SQL Server.",
        "skills": ["C#", ".NET Core", "ASP.NET", "SQL Server", "SQL", "Entity Framework", "REST APIs", "Git"],
        "experience_years": 1.5,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Information Systems", "institution": "Central Valley Institute", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior .NET Developer",
                "company": "IronClad Software",
                "duration": "2024 - Present (1.5 years)",
                "responsibilities": [
                    "Developed backend web APIs with C# and ASP.NET Core.",
                    "Wrote SQL queries and configured Entity Framework database contexts.",
                    "Maintained code using Git."
                ]
            }
        ],
        "projects": [
            {
                "name": "Corporate Employee Directory",
                "description": "Internal REST API service for organization role hierarchy and identity.",
                "technologies": ["C#", ".NET Core", "SQL Server", "Git"]
            }
        ],
        "certifications": []
    },
    {
        "candidate_id": "C015",
        "name": "Candidate C015",
        "professional_summary": "Machine Learning Engineer with 1.5 years of experience training predictive models and deploying inference APIs using Python, Scikit-Learn, PyTorch, Pandas, and FastAPI.",
        "skills": ["Python", "Machine Learning", "Scikit-Learn", "PyTorch", "Pandas", "NumPy", "FastAPI", "SQL", "Git"],
        "experience_years": 1.5,
        "education": {"degree": "Bachelor of Science", "field_of_study": "Data Science", "institution": "Pinnacle Institute", "graduation_year": 2024},
        "work_experience": [
            {
                "title": "Junior ML Engineer",
                "company": "Synthetix AI",
                "duration": "2024 - Present (1.5 years)",
                "responsibilities": [
                    "Trained and evaluated tabular machine learning models in Python.",
                    "Built lightweight FastAPI wrapper endpoints to serve model predictions.",
                    "Processed dataset features using Pandas and NumPy."
                ]
            }
        ],
        "projects": [
            {
                "name": "Predictive Lead Scoring API",
                "description": "FastAPI service serving real-time lead conversion probability scores.",
                "technologies": ["Python", "FastAPI", "Scikit-Learn", "Pandas"]
            }
        ],
        "certifications": []
    }
]

# Write resumes.json
with open(SAMPLE_DIR / "resumes.json", "w", encoding="utf-8") as f:
    json.dump(CANDIDATES, f, indent=2)
print(f"[OK] Wrote {len(CANDIDATES)} candidates to {SAMPLE_DIR / 'resumes.json'}")

# Write individual text resumes
for c in CANDIDATES:
    cid = c["candidate_id"]
    txt_path = RESUMES_DIR / f"{cid}.txt"
    lines = [
        f"CANDIDATE ID: {cid}",
        f"CANDIDATE NAME: {c['name']}",
        f"CONTACT: candidate.{cid.lower()}@synthetic-dataset.local | Synthetic Region",
        "",
        "=" * 80,
        "PROFESSIONAL SUMMARY",
        "=" * 80,
        c["professional_summary"],
        "",
        "=" * 80,
        "TECHNICAL SKILLS",
        "=" * 80,
        ", ".join(c["skills"]),
        "",
        "=" * 80,
        "PROFESSIONAL EXPERIENCE",
        "=" * 80,
    ]
    if not c["work_experience"]:
        lines.append("None (Entry-level / project experience only)")
    else:
        for w in c["work_experience"]:
            lines.append(f"{w['title']} | {w['company']}")
            lines.append(f"Duration: {w['duration']}")
            for resp in w["responsibilities"]:
                lines.append(f"- {resp}")
            lines.append("")
    lines.append(f"Total Professional Experience: {c['experience_years']} years")
    lines.append("")

    lines.append("=" * 80)
    lines.append("PROJECTS")
    lines.append("=" * 80)
    for p in c["projects"]:
        lines.append(f"Project: {p['name']}")
        lines.append(f"Description: {p['description']}")
        lines.append(f"Technologies: {', '.join(p['technologies'])}")
        lines.append("")

    lines.append("=" * 80)
    lines.append("EDUCATION")
    lines.append("=" * 80)
    edu = c["education"]
    lines.append(f"{edu['degree']} in {edu['field_of_study']}")
    lines.append(f"{edu['institution']} | Graduation Year: {edu['graduation_year']}")
    lines.append("")

    lines.append("=" * 80)
    lines.append("CERTIFICATIONS")
    lines.append("=" * 80)
    if c["certifications"]:
        for cert in c["certifications"]:
            lines.append(f"- {cert}")
    else:
        lines.append("None")

    txt_path.write_text("\n".join(lines), encoding="utf-8")

print(f"[OK] Generated {len(CANDIDATES)} plain-text resume files in {RESUMES_DIR}")

# Generate ground_truth.csv
GROUND_TRUTH_ROWS = [
    # Job 1: Junior Python Backend Developer
    ("JOB_001_PY_BACKEND", "C001", 5, "Strong match: Meets all requirements (Python, FastAPI, SQL, REST APIs, Git, Pytest) with 2 yrs exp."),
    ("JOB_001_PY_BACKEND", "C002", 4, "Strong partial match: 2 yrs Python backend, Django, SQL, REST APIs; lacks FastAPI."),
    ("JOB_001_PY_BACKEND", "C004", 3, "Project match: Strong Python/FastAPI capstone projects, but 0 yrs professional exp (tests min-experience filter)."),
    ("JOB_001_PY_BACKEND", "C007", 3, "Moderate match: 1.5 yrs Python, Flask, SQL, REST APIs; general full-stack background."),
    ("JOB_001_PY_BACKEND", "C013", 3, "Moderate match: 1.5 yrs Python, FastAPI, REST APIs; primarily MongoDB rather than SQL."),
    ("JOB_001_PY_BACKEND", "C015", 3, "Moderate match: Python and FastAPI serving experience, but ML focused."),
    ("JOB_001_PY_BACKEND", "C010", 2, "Weak match: 2 yrs Python and Pytest API testing, but QA rather than backend development."),
    ("JOB_001_PY_BACKEND", "C006", 2, "Weak match: 2 yrs Python and SQL, but focused on data pipelines/ETL rather than REST APIs."),
    ("JOB_001_PY_BACKEND", "C003", 2, "Weak match: 2 yrs enterprise backend with SQL and REST APIs, but in Java/Spring Boot without Python."),
    ("JOB_001_PY_BACKEND", "C008", 2, "Weak match: DevOps and container automation with Python scripting; light on backend API engineering."),
    ("JOB_001_PY_BACKEND", "C009", 4, "Overqualified: 6 yrs senior experience across FastAPI, PostgreSQL, and microservices."),
    ("JOB_001_PY_BACKEND", "C014", 2, "Weak match: Backend developer with SQL and REST APIs, but in C#/.NET rather than Python."),
    ("JOB_001_PY_BACKEND", "C011", 1, "Very weak match: Data analyst with SQL and BI dashboards; little software development."),
    ("JOB_001_PY_BACKEND", "C012", 1, "Very weak match: Mobile developer (Flutter/Dart); no Python or backend services."),
    ("JOB_001_PY_BACKEND", "C005", 1, "Very weak match: Frontend web developer (React/CSS/JS); minimal backend relevance."),

    # Job 2: Junior Python Data Engineer
    ("JOB_002_DATA_ENG", "C006", 5, "Strong match: Meets all requirements (Python, SQL, ETL, Pandas, Airflow, PostgreSQL, 2 yrs exp)."),
    ("JOB_002_DATA_ENG", "C011", 4, "Strong partial match: 1.5 yrs SQL, Pandas, data transformations; analytics background transitioning to pipeline engineering."),
    ("JOB_002_DATA_ENG", "C015", 4, "Strong partial match: 1.5 yrs Python, Pandas, data preprocessing and ML model pipelines; easily adapts to ETL."),
    ("JOB_002_DATA_ENG", "C001", 3, "Moderate match: Strong Python and PostgreSQL/SQL skills, but backend API rather than data pipelines."),
    ("JOB_002_DATA_ENG", "C002", 3, "Moderate match: 2 yrs Python and PostgreSQL SQL experience, but web application focused."),
    ("JOB_002_DATA_ENG", "C009", 3, "Overqualified / Adjacent: Senior backend architect with deep Python & PostgreSQL, but enterprise microservices focus."),
    ("JOB_002_DATA_ENG", "C004", 2, "Weak match: Python and SQL projects, but 0 yrs experience and lacks ETL/Pandas focus."),
    ("JOB_002_DATA_ENG", "C007", 2, "Weak match: Lightweight Flask/SQLite web developer; no data pipeline or ETL engineering."),
    ("JOB_002_DATA_ENG", "C008", 2, "Weak match: DevOps engineer with Python scripting; cloud infra focused rather than data pipelines."),
    ("JOB_002_DATA_ENG", "C010", 2, "Weak match: QA automation with Python; test automation rather than data engineering."),
    ("JOB_002_DATA_ENG", "C013", 2, "Weak match: Python backend developer with MongoDB/NoSQL focus; lacks relational SQL and ETL."),
    ("JOB_002_DATA_ENG", "C003", 1, "Very weak match: Java/Spring Boot backend; no Python, Pandas, or ETL pipeline experience."),
    ("JOB_002_DATA_ENG", "C005", 1, "Very weak match: Frontend React developer with no data engineering background."),
    ("JOB_002_DATA_ENG", "C012", 1, "Very weak match: Mobile developer (Flutter/Dart); no data engineering or Python relevance."),
    ("JOB_002_DATA_ENG", "C014", 1, "Very weak match: C#/.NET developer; no Python, Pandas, or data engineering tools.")
]

csv_path = SAMPLE_DIR / "ground_truth.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["job_id", "candidate_id", "relevance_1_to_5", "reason"])
    for row in GROUND_TRUTH_ROWS:
        writer.writerow(row)

print(f"[OK] Wrote {len(GROUND_TRUTH_ROWS)} ground truth rows to {csv_path}")
