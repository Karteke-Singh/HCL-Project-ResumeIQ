import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.session import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    jd_text = Column(Text, nullable=False)
    requirements_json = Column(Text, nullable=False)
    weights_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidates = relationship("Candidate", back_populates="job", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="job", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String(36), ForeignKey("jobs.id"), nullable=False)
    display_id = Column(String(50), nullable=False)  # e.g., C001
    masked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="candidates")
    resume = relationship("Resume", back_populates="candidate", uselist=False, cascade="all, delete-orphan")
    profile = relationship("Profile", back_populates="candidate", uselist=False, cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="candidate", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id = Column(String(36), ForeignKey("candidates.id"), unique=True, nullable=False)
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)

    candidate = relationship("Candidate", back_populates="resume")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id = Column(String(36), ForeignKey("candidates.id"), unique=True, nullable=False)
    skills = Column(Text, nullable=False)  # JSON array string
    experience_years = Column(Float, default=0.0)
    education = Column(Text, nullable=True)  # JSON object string
    projects = Column(Text, nullable=True)  # JSON array string
    certifications = Column(Text, nullable=True)  # JSON array string
    professional_summary = Column(Text, nullable=True)

    candidate = relationship("Candidate", back_populates="profile")


class Score(Base):
    __tablename__ = "scores"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id = Column(String(36), ForeignKey("candidates.id"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id"), nullable=False)
    rule = Column(Float, default=0.0)
    semantic = Column(Float, default=0.0)
    experience = Column(Float, default=0.0)
    llm_fit = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    passed_hard_requirements = Column(Boolean, default=True)
    explanation = Column(Text, nullable=True)
    matched_skills = Column(Text, nullable=True)  # JSON array string
    missing_skills = Column(Text, nullable=True)  # JSON array string
    evidence = Column(Text, nullable=True)  # JSON array string

    candidate = relationship("Candidate", back_populates="scores")
    job = relationship("Job", back_populates="scores")
