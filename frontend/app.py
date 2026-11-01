
import requests
import pandas as pd
import streamlit as st

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="ResumeIQ | P_101",
    page_icon="📄",
    layout="wide",
)

API = "http://127.0.0.1:8000"

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.8rem;
}
.hero {
    padding: 28px;
    border-radius: 16px;
    background: linear-gradient(120deg, #102A43, #176B87);
    color: white;
    margin-bottom: 24px;
}
.hero h1 {
    color: white;
    font-size: 38px;
}
.hero p {
    color: #E0F2FE;
}
div[data-testid="stMetric"] {
    background: rgba(128,128,128,0.08);
    padding: 16px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.2);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>📄 ResumeIQ</h1>
    <p>LLM-Based Resume Screening System | Project P_101</p>
    <p>Hybrid Screening • Explainable Results • Human Review</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("ResumeIQ")
st.sidebar.caption("Project P_101")
st.sidebar.info("Connected to your local FastAPI backend.")
st.sidebar.warning(
    "Scores support human review and must not make hiring "
    "decisions automatically."
)

# ---------------- LOAD JOBS ----------------
st.header("1. Select Job Position")

try:
    response = requests.get(f"{API}/api/v1/jobs", timeout=10)
    response.raise_for_status()
    payload = response.json()
    jobs = payload.get("result", [])

except requests.RequestException:
    st.error(
        "Cannot connect to the backend. Start FastAPI in another "
        "terminal using: python -m uvicorn backend.app.main:app --reload"
    )
    st.stop()

if not jobs:
    st.warning("No job positions are available.")
    st.stop()

job_options = {
    f"{job['title']} ({job['id']})": job["id"]
    for job in jobs
}

selected_job_label = st.selectbox(
    "Choose a job",
    list(job_options.keys()),
)
job_id = job_options[selected_job_label]

try:
    job_response = requests.get(
        f"{API}/api/v1/jobs/{job_id}",
        timeout=10,
    )
    job_response.raise_for_status()
    job_details = job_response.json()["result"]

    with st.expander("View job description and requirements"):
        st.write(job_details.get("description", ""))

        requirements = job_details.get("requirements", {})
        st.write("**Mandatory skills**")
        st.write(", ".join(
            requirements.get("must_have_skills", [])
        ) or "Not specified")

        st.write("**Nice-to-have skills**")
        st.write(", ".join(
            requirements.get("nice_to_have_skills", [])
        ) or "Not specified")

        st.write(
            "**Minimum experience:** "
            f"{requirements.get('minimum_experience_years', 0)} years"
        )

except (requests.RequestException, KeyError, ValueError):
    st.warning("Could not load the full job description.")

# ---------------- UPLOAD RESUMES ----------------
st.divider()
st.header("2. Upload Resumes")

uploaded_files = st.file_uploader(
    "Choose resume files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="Maximum 20 files, each up to 10 MB.",
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} resume(s) selected.")

# ---------------- SCREENING ----------------
if st.button(
    "🚀 Start Resume Screening",
    type="primary",
    use_container_width=True,
):
    if not uploaded_files:
        st.warning("Please upload at least one resume.")

    elif len(uploaded_files) > 20:
        st.error("Upload a maximum of 20 resumes.")

    else:
        results = []
        failures = []

        progress = st.progress(0)
        status = st.empty()

        mime_types = {
            "pdf": "application/pdf",
            "docx": (
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            "txt": "text/plain",
        }

        for index, uploaded_file in enumerate(uploaded_files):
            filename = uploaded_file.name
            file_bytes = uploaded_file.getvalue()

            status.write(
                f"Processing {index + 1}/{len(uploaded_files)}: "
                f"{filename}"
            )

            extension = filename.rsplit(".", 1)[-1].lower()

            if not file_bytes:
                failures.append({
                    "Resume": filename,
                    "Error": "Empty file",
                })

            elif len(file_bytes) > 10 * 1024 * 1024:
                failures.append({
                    "Resume": filename,
                    "Error": "File exceeds 10 MB",
                })

            else:
                try:
                    api_response = requests.post(
                        f"{API}/api/v1/screening/single",
                        data={"job_id": job_id},
                        files={
                            "file": (
                                filename,
                                file_bytes,
                                mime_types[extension],
                            )
                        },
                        timeout=120,
                    )

                    if api_response.ok:
                        item = api_response.json()["result"]
                        item["filename"] = filename
                        results.append(item)
                    else:
                        try:
                            error = api_response.json().get(
                                "detail", "Screening failed"
                            )
                        except ValueError:
                            error = "Screening failed"

                        failures.append({
                            "Resume": filename,
                            "Error": str(error),
                        })

                except requests.RequestException as exc:
                    failures.append({
                        "Resume": filename,
                        "Error": str(exc),
                    })

            progress.progress((index + 1) / len(uploaded_files))

        progress.empty()
        status.empty()

        st.session_state["results"] = results
        st.session_state["failures"] = failures
        st.session_state["results_job_id"] = job_id

# ---------------- DISPLAY RESULTS ----------------
if (
    "results" in st.session_state
    and st.session_state.get("results_job_id") == job_id
):
    results = st.session_state["results"]
    failures = st.session_state["failures"]

    st.divider()
    st.header("3. Screening Dashboard")

    if results:
        results = sorted(
            results,
            key=lambda x: x.get("scores", {}).get("total_score", 0),
            reverse=True,
        )

        average = sum(
            x.get("scores", {}).get("total_score", 0)
            for x in results
        ) / len(results)

        passed = sum(
            bool(x.get("scores", {}).get(
                "passed_hard_requirements", False
            ))
            for x in results
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Resumes Screened", len(results))
        col2.metric("Hard Requirements Passed", passed)
        col3.metric("Average Score", f"{average:.1f}/100")

        rows = []

        for item in results:
            scores = item.get("scores", {})

            rows.append({
                "Candidate ID": item.get("candidate_id", "Unknown"),
                "Resume": item.get("filename", ""),
                "Score / 100": scores.get("total_score", 0),
                "Requirements Passed": (
                    "Yes" if scores.get(
                        "passed_hard_requirements", False
                    ) else "No"
                ),
                "Experience Passed": (
                    "Yes" if item.get("experience_passed", False)
                    else "No"
                ),
                "Matched Skills": ", ".join(
                    item.get("matched_skills", [])
                ),
                "Missing Skills": ", ".join(
                    item.get("missing_skills", [])
                ),
            })

        comparison = pd.DataFrame(rows)

        st.subheader("Candidate Comparison")
        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download Results as CSV",
            data=comparison.to_csv(index=False).encode("utf-8"),
            file_name="resume_screening_results.csv",
            mime="text/csv",
        )

        st.subheader("Score Comparison")
        chart_data = comparison.set_index("Candidate ID")[
            ["Score / 100"]
        ]
        st.bar_chart(chart_data)

        st.subheader("Candidate Explanations and Evidence")

        for position, item in enumerate(results, start=1):
            scores = item.get("scores", {})
            candidate_id = item.get("candidate_id", "Unknown")
            score = scores.get("total_score", 0)

            with st.expander(
                f"{position}. {candidate_id} — {score}/100"
            ):
                st.write("**Resume:**", item.get("filename", ""))
                st.write(
                    "**Display name:**",
                    item.get("display_name", "Unknown"),
                )
                st.write("**Score breakdown:**", scores)

                st.write(
                    "**Matched skills:**",
                    ", ".join(item.get("matched_skills", []))
                    or "None reported",
                )
                st.write(
                    "**Missing skills:**",
                    ", ".join(item.get("missing_skills", []))
                    or "None reported",
                )

                st.write("**Explanation:**")
                st.write(
                    item.get("explanation", "No explanation available.")
                )

                st.write("**Evidence snippets:**")
                evidence = item.get("evidence_snippets", [])

                if evidence:
                    for snippet in evidence:
                        st.info(snippet)
                else:
                    st.write("No evidence snippets returned.")

                if item.get("llm_reason"):
                    st.caption(
                        "Fit-rating reason: " + item["llm_reason"]
                    )

                for warning in item.get("warnings", []):
                    st.warning(warning)

    else:
        st.warning("No resumes were successfully screened.")

    if failures:
        st.subheader("Files That Could Not Be Screened")
        st.dataframe(
            pd.DataFrame(failures),
            use_container_width=True,
            hide_index=True,
        )

st.divider()
st.caption(
    "ResumeIQ | P_101 | Screening results require human verification. "
    "Scores must not be the sole basis for hiring decisions."
)
