import os
from pathlib import Path
from dataclasses import dataclass, field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


@dataclass
class Settings:
    PROJECT_NAME: str = "LLM-Based Resume Screening System"
    PROJECT_ID: str = "P_101"
    STUDENT_NAME: str = "Rishi Singh"
    REPO_NAME: str = "p101-resume-screening-llm-rishi-singh"

    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    SAMPLE_DATA_DIR: Path = BASE_DIR / "data" / "sample"
    RAW_DATA_DIR: Path = BASE_DIR / "data" / "raw"
    DOCS_DIR: Path = BASE_DIR / "docs"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'resume_screener.db'}")

    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock")  # gemini, groq, openai, mock
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")

    # Hybrid Scoring Default Weights
    WEIGHT_RULE: float = float(os.getenv("DEFAULT_RULE_WEIGHT", "0.3"))
    WEIGHT_SEMANTIC: float = float(os.getenv("DEFAULT_SEMANTIC_WEIGHT", "0.4"))
    WEIGHT_EXPERIENCE: float = float(os.getenv("DEFAULT_EXPERIENCE_WEIGHT", "0.2"))
    WEIGHT_LLM_FIT: float = float(os.getenv("DEFAULT_LLM_FIT_WEIGHT", "0.1"))


settings = Settings()
