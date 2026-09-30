from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# --- Education & Project Models ---
class EducationItem(BaseModel):
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[int] = None


class WorkExperienceItem(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)


class ProjectItem(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)


# --- Parsed Profile Model ---
class ParsedProfile(BaseModel):
    candidate_id: str
    name: Optional[str] = None
    professional_summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experience_years: float = 0.0
    education: Optional[EducationItem] = None
    work_experience: List[WorkExperienceItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)


# --- Job Models ---
class JobRequirements(BaseModel):
    must_have_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)
    minimum_experience_years: float = 0.0
    preferred_education: Optional[str] = None
    key_responsibilities: List[str] = Field(default_factory=list)


class ScoringWeights(BaseModel):
    rule: float = 0.3
    semantic: float = 0.4
    experience: float = 0.2
    llm_fit: float = 0.1


class JobCreate(BaseModel):
    title: str
    jd_text: str
    requirements: Optional[JobRequirements] = None
    weights: Optional[ScoringWeights] = None


class JobResponse(BaseModel):
    id: str
    title: str
    jd_text: str
    requirements: JobRequirements
    weights: ScoringWeights


# --- Scoring & Ranking Models ---
class ScoreBreakdown(BaseModel):
    rule_score: float  # 0.0 - 1.0 (pass/fail gates + mandatory overlap)
    semantic_score: float  # 0.0 - 1.0 (cosine similarity / skills overlap)
    experience_score: float  # 0.0 - 1.0 (ratio of exp vs required)
    llm_fit_score: float  # 0.0 - 1.0 (qualitative fit rating)
    total_score: float  # weighted sum (0 - 100 or 0.0 - 1.0)
    passed_hard_requirements: bool


class CandidateRanking(BaseModel):
    candidate_id: str
    display_id: str
    display_name: str
    scores: ScoreBreakdown
    matched_skills: List[str]
    missing_skills: List[str]
    evidence_snippets: List[str]
    explanation: str
    is_masked: bool = False


class ScreeningResponse(BaseModel):
    job_id: str
    total_screened: int
    rankings: List[CandidateRanking]
