
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.db.session import get_db

router = APIRouter()


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "success": True,
            "result": {
                "status": "healthy",
                "database": "connected"
            },
            "warnings": []
        }

    except Exception:
        return {
            "success": False,
            "result": {
                "status": "unhealthy",
                "database": "disconnected"
            },
            "warnings": ["Database connection failed"]
        }
