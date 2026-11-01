
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.db.models import Job
from backend.app.services.text_extractor import extract_text_from_bytes
from backend.app.services.screening_service import screening_service

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024


@router.post("/screening/single")
async def screen_single_resume(
    job_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Check the job.
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")

    # Check the file extension.
    filename = file.filename or "resume"
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Upload a PDF, DOCX, or TXT resume.",
        )

    # Read and validate the file size.
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="The file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The file exceeds the 10 MB limit.",
        )

    # Extract the resume text.
    raw_text = extract_text_from_bytes(file_bytes, filename)

    if raw_text.startswith("Error extracting") or not raw_text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract readable text from the resume.",
        )

    # Run the screening service.
    try:
        result = screening_service.screen_resume(job, raw_text)
    except Exception as exc:
        # Keep internal error details out of the API response.
        raise HTTPException(
            status_code=500,
            detail="Resume screening failed. Check the server terminal.",
        ) from exc

    return {
        "success": True,
        "result": result,
        "warnings": result.get("warnings", []),
    }
