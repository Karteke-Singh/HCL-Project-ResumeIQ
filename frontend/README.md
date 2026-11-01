# ResumeScreenAI React frontend (P_101)

React + Vite UI for the existing FastAPI resume screening backend. Designed to be copied into the existing repository's `frontend/` directory; it does not touch your SQLite database.

## Run locally
1. Install Node.js (20+ recommended).
2. Copy this folder's contents into your repository's `frontend/` folder. Back up the existing Streamlit files first if you want to keep them.
3. In PowerShell, open the `frontend` folder and run:
   ```powershell
   npm install
   Copy-Item .env.example .env
   npm run dev
   ```
4. Open `http://127.0.0.1:5173`.
5. In a separate PowerShell window, run the backend from the repository root:
   ```powershell
   python -m uvicorn backend.app.main:app --reload
   ```

Uses `GET /api/v1/health`, `GET /api/v1/jobs`, `GET /api/v1/jobs/{job_id}`, and `POST /api/v1/screening/single`. Multiple resumes are submitted one at a time because the existing API is a single-resume endpoint. Set `VITE_API_BASE_URL` in `.env` if the backend URL differs.

The Create Job screen is a non-persistent draft: the backend endpoints shared so far do not include `POST /api/v1/jobs`. All scores are decision support only and require human review.
