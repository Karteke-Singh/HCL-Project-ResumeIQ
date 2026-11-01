from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db.session import init_db
from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.jobs import router as jobs_router
from backend.app.api.routes.resumes import router as resumes_router
from backend.app.api.routes.screening import router as screening_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="LLM-Based Resume Screening System",
    description="API for hybrid resume screening and job matching.",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the local React/Vite frontend to access FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes.
app.include_router(health_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(resumes_router, prefix="/api/v1")
app.include_router(screening_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "success": True,
        "result": {
            "project": "LLM-Based Resume Screening System",
            "project_id": "P_101",
            "status": "running",
        },
        "warnings": [],
    }