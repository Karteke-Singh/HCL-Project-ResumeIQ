
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.db.models import Job
from backend.app.services.text_extractor import extract_text_from_bytes
from backend.app.services.resume_parser import resume_parser_v1

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/resumes/preview")
async def preview_resume(
    job_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 1. Validate the selected job.
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    # 2. Validate the file extension.
    filename = file.filename or "resume"
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Upload a PDF, DOCX, or TXT file.",
        )

    # 3. Read the file and check its size.
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The file exceeds the 10 MB limit.",
        )

    # 4. Extract text using the existing extractor.
    raw_text = extract_text_from_bytes(file_bytes, filename)

    if raw_text.startswith("Error extracting"):
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from this file.",
        )

    if not raw_text.strip():
        raise HTTPException(
            status_code=422,
            detail=(
                "No readable text was found. "
                "The PDF may be scanned and require OCR."
            ),
        )

    # 5. Parse the resume using the existing parser.
    try:
        profile = resume_parser_v1.parse(raw_text)
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail="Resume parsing failed.",
        ) from exc

    # 6. Return the preview without saving candidate data.
    return {
        "success": True,
        "result": {
            "job_id": job.id,
            "job_title": job.title,
            "filename": filename,
            "extracted_characters": len(raw_text),
            "parsed_profile": profile.model_dump(mode="json"),
        },
        "warnings": [
            "Review extracted information for accuracy.",
            "This preview does not save the resume or make a hiring decision.",
        ],
    }
