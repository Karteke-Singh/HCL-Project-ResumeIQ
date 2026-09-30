import re
from typing import Dict, List, Optional, Any
from backend.app.schemas import ParsedProfile, EducationItem, WorkExperienceItem, ProjectItem

# Comprehensive Skills Taxonomy
SKILLS_TAXONOMY = {
    "Languages": ["python", "java", "c#", "javascript", "typescript", "dart", "sql", "bash", "html", "html5", "css", "css3"],
    "Frameworks & Libraries": ["fastapi", "django", "django rest framework", "flask", "spring boot", "react", "redux", "flutter", "pandas", "numpy", "scikit-learn", "pytorch", "pydantic", "sqlalchemy", "entity framework", "asp.net"],
    "Databases": ["postgresql", "mysql", "sqlite", "mongodb", "redis", "sql server", "firebase"],
    "Testing": ["pytest", "junit", "mockito", "selenium", "automated testing", "api testing"],
    "DevOps & Tools": ["git", "docker", "kubernetes", "aws", "ci/cd", "maven", "webpack", "tailwind css", "airflow", "apache airflow", "terraform", "linux"],
    "Concepts & Domains": ["rest apis", "restful apis", "microservices", "etl", "data modeling", "data analysis", "machine learning"]
}

# Flattened set for rapid lookup
ALL_TAXONOMY_SKILLS = [skill for cat in SKILLS_TAXONOMY.values() for skill in cat]


class ResumeParserV1:
    """
    Resume Parser v1 using structured regex rules, section splitting,
    and technical skills taxonomy matching.
    """

    def parse(self, raw_text: str, candidate_id_hint: Optional[str] = None) -> ParsedProfile:
        candidate_id = self._extract_candidate_id(raw_text, candidate_id_hint)
        name = self._extract_name(raw_text, candidate_id)
        sections = self._split_sections(raw_text)

        summary = self._extract_summary(sections, raw_text)
        skills = self._extract_skills(sections, raw_text)
        exp_years = self._extract_experience_years(sections, raw_text)
        education = self._extract_education(sections, raw_text)
        projects = self._extract_projects(sections)
        certifications = self._extract_certifications(sections)

        return ParsedProfile(
            candidate_id=candidate_id,
            name=name,
            professional_summary=summary,
            skills=skills,
            experience_years=exp_years,
            education=education,
            work_experience=[],  # v1 focuses on summary & years; structured roles optional
            projects=projects,
            certifications=certifications
        )

    def _extract_candidate_id(self, text: str, hint: Optional[str] = None) -> str:
        if hint:
            return hint
        match = re.search(r"CANDIDATE\s+ID:\s*([A-Za-z0-9_-]+)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match_alt = re.search(r"\b(C\d{3,4})\b", text)
        if match_alt:
            return match_alt.group(1).strip()
        return "UNKNOWN"

    def _extract_name(self, text: str, candidate_id: str) -> str:
        match = re.search(r"CANDIDATE\s+NAME:\s*([^\n\r]+)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return f"Candidate {candidate_id}"

    def _split_sections(self, text: str) -> Dict[str, str]:
        section_headers = [
            "PROFESSIONAL SUMMARY",
            "SUMMARY",
            "TECHNICAL SKILLS",
            "SKILLS",
            "PROFESSIONAL EXPERIENCE",
            "WORK EXPERIENCE",
            "EXPERIENCE",
            "PROJECTS",
            "EDUCATION",
            "CERTIFICATIONS"
        ]
        pattern = r"(?:^|\n)(?:\={3,80}\s*)?(" + "|".join(section_headers) + r")(?:\s*\={3,80})?(?:\n|:)"
        parts = re.split(pattern, text, flags=re.IGNORECASE)

        sections = {}
        if len(parts) > 1:
            for i in range(1, len(parts), 2):
                header = parts[i].strip().upper()
                content = parts[i + 1].strip() if i + 1 < len(parts) else ""
                sections[header] = content
        return sections

    def _extract_summary(self, sections: Dict[str, str], full_text: str) -> Optional[str]:
        for k in ["PROFESSIONAL SUMMARY", "SUMMARY"]:
            if k in sections and sections[k]:
                return sections[k].strip()
        return None

    def _extract_skills(self, sections: Dict[str, str], full_text: str) -> List[str]:
        found_skills = set()
        skills_text = ""
        for k in ["TECHNICAL SKILLS", "SKILLS"]:
            if k in sections:
                skills_text += " " + sections[k]

        text_to_search = skills_text if skills_text.strip() else full_text
        lower_text = text_to_search.lower()

        for skill in ALL_TAXONOMY_SKILLS:
            # Word boundary regex with special char support (e.g., C#, CI/CD)
            escaped = re.escape(skill)
            pattern = rf"(?<!\w){escaped}(?!\w)"
            if re.search(pattern, lower_text):
                found_skills.add(self._canonical_name(skill))

        return sorted(list(found_skills))

    def _canonical_name(self, skill: str) -> str:
        mapping = {
            "python": "Python",
            "fastapi": "FastAPI",
            "django": "Django",
            "django rest framework": "Django REST Framework",
            "flask": "Flask",
            "java": "Java",
            "spring boot": "Spring Boot",
            "c#": "C#",
            "javascript": "JavaScript",
            "typescript": "TypeScript",
            "dart": "Dart",
            "sql": "SQL",
            "postgresql": "PostgreSQL",
            "mysql": "MySQL",
            "sqlite": "SQLite",
            "mongodb": "MongoDB",
            "redis": "Redis",
            "sql server": "SQL Server",
            "firebase": "Firebase",
            "rest apis": "REST APIs",
            "restful apis": "REST APIs",
            "pytest": "Pytest",
            "junit": "JUnit",
            "selenium": "Selenium",
            "automated testing": "Automated Testing",
            "git": "Git",
            "docker": "Docker",
            "kubernetes": "Kubernetes",
            "aws": "AWS",
            "ci/cd": "CI/CD",
            "react": "React",
            "html": "HTML5",
            "html5": "HTML5",
            "css": "CSS3",
            "css3": "CSS3",
            "tailwind css": "Tailwind CSS",
            "pandas": "Pandas",
            "numpy": "NumPy",
            "scikit-learn": "Scikit-Learn",
            "pytorch": "PyTorch",
            "airflow": "Apache Airflow",
            "apache airflow": "Apache Airflow",
            "etl": "ETL",
            "data modeling": "Data Modeling",
            "data analysis": "Data Analysis",
            "pydantic": "Pydantic",
            "flutter": "Flutter",
            "bash": "Bash",
            "linux": "Linux"
        }
        return mapping.get(skill.lower(), skill.title())

    def _extract_experience_years(self, sections: Dict[str, str], full_text: str) -> float:
        # Match explicit "Total Professional Experience: X years"
        m = re.search(r"Total\s+Professional\s+Experience:\s*([0-9]+(?:\.[0-9]+)?)\s*years?", full_text, re.IGNORECASE)
        if m:
            return float(m.group(1))

        # Check in experience section or full text for "X years of experience"
        text_to_search = sections.get("PROFESSIONAL EXPERIENCE") or sections.get("EXPERIENCE") or full_text
        m2 = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(?:\+)?\s*years?\s*(?:of\s*(?:professional\s*)?experience)?", text_to_search, re.IGNORECASE)
        if m2:
            return float(m2.group(1))

        # Check for zero experience indicator
        if re.search(r"(?:0\s*years|no\s*(?:formal|prior|professional)\s*experience|entry-level)", text_to_search, re.IGNORECASE):
            return 0.0

        return 0.0

    def _extract_education(self, sections: Dict[str, str], full_text: str) -> Optional[EducationItem]:
        edu_text = sections.get("EDUCATION", "")
        if not edu_text:
            return None

        degree_match = re.search(r"(Bachelor\s+(?:of\s+[A-Za-z]+)?|Master\s+(?:of\s+[A-Za-z]+)?|B\.S\.|M\.S\.|B\.Tech|Ph\.D\.)(?:\s+in\s+([^\n\r\|]+))?", edu_text, re.IGNORECASE)
        institution_match = re.search(r"([A-Za-z\s]+(?:University|College|Institute|Academy|School))", edu_text, re.IGNORECASE)
        year_match = re.search(r"(?:Graduation\s+Year:\s*|in\s*|Class\s+of\s*)(\b20[12][0-9]\b)", edu_text, re.IGNORECASE)

        return EducationItem(
            degree=degree_match.group(1).strip() if degree_match else "Bachelor's Degree",
            field_of_study=degree_match.group(2).strip() if (degree_match and degree_match.group(2)) else None,
            institution=institution_match.group(1).strip() if institution_match else None,
            graduation_year=int(year_match.group(1)) if year_match else None
        )

    def _extract_projects(self, sections: Dict[str, str]) -> List[ProjectItem]:
        proj_text = sections.get("PROJECTS", "")
        if not proj_text:
            return []

        projects = []
        blocks = re.split(r"(?:Project:\s*|\d+\.\s+)", proj_text)
        for b in blocks:
            lines = [line.strip() for line in b.split("\n") if line.strip()]
            if not lines:
                continue
            name = lines[0]
            desc = ""
            techs = []
            for l in lines[1:]:
                if l.lower().startswith("description:"):
                    desc = l.split(":", 1)[1].strip()
                elif l.lower().startswith("technologies:"):
                    raw_tech = l.split(":", 1)[1].strip()
                    techs = [t.strip() for t in raw_tech.split(",") if t.strip()]
            projects.append(ProjectItem(name=name, description=desc, technologies=techs))
        return projects

    def _extract_certifications(self, sections: Dict[str, str]) -> List[str]:
        cert_text = sections.get("CERTIFICATIONS", "")
        if not cert_text or cert_text.strip().lower() in ["none", "n/a"]:
            return []
        items = []
        for line in cert_text.split("\n"):
            line = line.strip().lstrip("-").lstrip("*").strip()
            if line and line.lower() not in ["none", "n/a"]:
                items.append(line)
        return items


resume_parser_v1 = ResumeParserV1()
