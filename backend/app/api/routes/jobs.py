
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.db.models import Job

router = APIRouter()


def parse_json(value):
    try:
        return json.loads(value) if value else {}
    except (json.JSONDecodeError, TypeError):
        return {}


@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()

    results = []

    for job in jobs:
        results.append({
            "id": job.id,
            "title": job.title,
            "requirements": parse_json(job.requirements_json),
            "created_at": (
                job.created_at.isoformat()
                if job.created_at else None
            )
        })

    return {
        "success": True,
        "result": results,
        "warnings": []
    }


@router.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "success": True,
        "result": {
            "id": job.id,
            "title": job.title,
            "description": job.jd_text,
            "requirements": parse_json(job.requirements_json),
            "weights": parse_json(job.weights_json),
            "created_at": (
                job.created_at.isoformat()
                if job.created_at else None
            )
        },
        "warnings": []
    }
