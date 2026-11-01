
import requests
import pandas as pd
import streamlit as st

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="ResumeIQ | Resume Screening",
    page_icon="📄",
    layout="wide",
)

API_BASE = "http://127.0.0.1:8000"

# --------------------------------------------------
# Styling
# --------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 26px;
        border-radius: 16px;
        background: linear-gradient(120deg, #102A43, #176B87);
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        margin-bottom: 8px;
    }

    .hero p {
        color: #E0F2FE;
        margin-bottom: 0;
    }

    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.07);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>📄 ResumeIQ</h1>
        <p>
            LLM-Based Resume Screening System · Project P_101
        </p>
        <p>
            Hybrid screening | Explainable results | Human review
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("⚙️ Configuration")
st.sidebar.caption("Connect to your local FastAPI backend.")

st.sidebar.code(API_BASE)

st.sidebar.info(
    "Your resume files are sent to your local screening API. "
    "This demo does not save newly uploaded resumes to the database."
)

st.sidebar.warning(
    "Screening scores support human review. "
    "They should not make hiring decisions automatically."
)

# --------------------------------------------------
# Load available jobs
# --------------------------------------------------
st.subheader("1. Select a job")

try:
    response = requests.get(
        f"{API_BASE}/api/v1/jobs",
        timeout=10,
    )
    response.raise_for_status()
    jobs_data = response.json()

    if not jobs_data.get("success"):
        st.error("The API did not return the job list.")
        st.stop()

    jobs = jobs_data.get("result", [])

except requests.RequestException as exc:
    st.error(
        "Cannot connect to FastAPI. Start the backend first "
        "and confirm that it is running on port 8000."
    )
    st.code(str(exc))
    st.stop()

if not jobs:
    st.warning("No jobs are available. Add a job before screening.")
    st.stop()

job_labels = {
    f"{job['title']} ({job['id']})": job["id"]
    for job in jobs
}

selected_label = st.selectbox(
    "Job position",
    options=list(job_labels.keys()),
)

selected_job_id = job_labels[selected_label]
selected_job = next(
    job for job in jobs
    if job["id"] == selected_job_id
)

with st.expander("View job details"):
    try:
        job_response = requests.get(
            f"{API_BASE}/api/v1/jobs/{selected_job_id}",
            timeout=10,
        )
        job_response.raise_for_status()
        job_details = job_response.json()["result"]

        st.write(job_details["description"])

        requirements = job_details.get("requirements", {})

        st.write("**Mandatory skills**")
        st.write(
            ", ".join(requirements.get("must_have_skills", []))
            or "Not specified"
        )

        st.write("**Nice-to-have skills**")
        st.write(
            ", ".join(requirements.get("nice_to_have_skills", []))
            or "Not specified"
        )

        st.write(
            "**Minimum experience:** "
            f"{requirements.get('minimum_experience_years', 0)} years"
        )

    except requests.RequestException as exc:
        st.warning(f"Could not load full job details: {exc}")

# --------------------------------------------------
# Upload resumes
# --------------------------------------------------
st.divider()
st.subheader("2. Upload resumes")

uploaded_files = st.file_uploader(
    "Choose PDF, DOCX, or TXT resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="Maximum 20 resumes per screening run, 10 MB each.",
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} resume(s) selected.")

# --------------------------------------------------
# Screen resumes
# --------------------------------------------------
if st.button(
    "🚀 Screen Resumes",
    type="primary",
    use_container_width=True,
):
    if not uploaded_files:
        st.warning("Please upload at least one resume.")
    elif len(uploaded_files) > 20:
        st.error("Please upload no more than 20 resumes.")
    else:
        results = []
        failures = []

        progress = st.progress(0)
        status = st.empty()

        for index, uploaded_file in enumerate(uploaded_files):
            filename = uploaded_file.name

            status.write(
                f"Screening {index + 1}/{len(uploaded_files)}: "
                f"{filename}"
            )

            file_bytes = uploaded_file.getvalue()

            if not file_bytes:
                failures.append({
                    "filename": filename,
                    "error": "The file is empty.",
                })
                progress.progress((index + 1) / len(uploaded_files))
                continue

            if len(file_bytes) > 10 * 1024 * 1024:
                failures.append({
                    "filename": filename,
                    "error": "The file exceeds 10 MB.",
                })
                progress.progress((index + 1) / len(uploaded_files))
                continue

            extension = filename.rsplit(".", 1)[-1].lower()

            mime_types = {
                "pdf": "application/pdf",
                "docx": (
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                "txt": "text/plain",
            }

            try:
                api_response = requests.post(
                    f"{API_BASE}/api/v1/screening/single",
                    data={"job_id": selected_job_id},
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
                    payload = api_response.json()
                    result = payload.get("result", {})

                    result["filename"] = filename
                    results.append(result)
                else:
                    try:
                        error_body = api_response.json()
                        error_message = error_body.get(
                            "detail",
                            "Screening request failed.",
                        )
                    except ValueError:
                        error_message = "Screening request failed."

                    failures.append({
                        "filename": filename,
                        "error": str(error_message),
                    })

            except requests.RequestException as exc:
                failures.append({
                    "filename": filename,
                    "error": str(exc),
                })

            progress.progress((index + 1) / len(uploaded_files))

        status.empty()
        progress.empty()

        # Store results for display after the run.
        st.session_state["screening_results"] = results
        st.session_state["screening_failures"] = failures
        st.session_state["screening_job_id"] = selected_job_id

        st.rerun()

# --------------------------------------------------
# Display results
# --------------------------------------------------
if (
    "screening_results" in st.session_state
    and st.session_state.get("screening_job_id") == selected_job_id
):
    results = st.session_state["screening_results"]
    failures = st.session_state["screening_failures"]

    st.divider()
    st.subheader("3. Screening dashboard")

    if results:
        # Sort by score for comparison, not as a hiring decision.
        results = sorted(
            results,
            key=lambda item: item.get("scores", {}).get(
                "total_score", 0
            ),
            reverse=True,
        )

        total_screened = len(results)
        passed_count = sum(
            item.get("scores", {}).get(
                "passed_hard_requirements", False
            )
            for item in results
        )
        average_score = sum(
            item.get("scores", {}).get("total_score", 0)
            for item in results
        ) / total_screened

        col1, col2, col3 = st.columns(3)

        col1.metric("Resumes screened", total_screened)
        col2.metric("Hard requirements passed", passed_count)
        col3.metric("Average score", f"{average_score:.1f}/100")

        st.caption(
            "Results are sorted by the configured screening score. "
            "Verify resume evidence and requirements before drawing conclusions."
        )

        # Build the comparison table.
        table_rows = []

        for item in results:
            scores = item.get("scores", {})

            table_rows.append({
                "Candidate ID": item.get("candidate_id", "Unknown"),
                "Resume": item.get("filename", ""),
                "Score / 100": scores.get("total_score", 0),
                "Requirements passed": (
                    "Yes"
                    if scores.get("passed_hard_requirements", False)
                    else "No"
                ),
                "Experience passed": (
                    "Yes"
                    if item.get("experience_passed", False)
                    else "No"
                ),
                "Matched skills": ", ".join(
                    item.get("matched_skills", [])
                ),
                "Missing skills": ", ".join(
                    item.get("missing_skills", [])
                ),
            })

        comparison_df = pd.DataFrame(table_rows)

        st.markdown("### Candidate comparison")
        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = comparison_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download comparison CSV",
            data=csv_data,
            file_name="resume_screening_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # Show details and evidence for each candidate.
        st.markdown("### Candidate details")

        for position, item in enumerate(results, start=1):
            scores = item.get("scores", {})
            candidate_id = item.get("candidate_id", "Unknown")
            score = scores.get("total_score", 0)

            with st.expander(
                f"{position}. {candidate_id} — {score}/100"
            ):
                left, right = st.columns(2)

                left.write(
                    f"**Resume:** {item.get('filename', '')}"
                )
                left.write(
                    "**Hard requirements:** "
                    + (
                        "Passed"
                        if scores.get(
                            "passed_hard_requirements", False
                        )
                        else "Not passed"
                    )
                )

                right.write(
                    f"**Name:** {item.get('display_name', 'Unknown')}"
                )
                right.write(
                    "**Experience requirement:** "
                    + (
                        "Met"
                        if item.get("experience_passed", False)
                        else "Not met"
                    )
                )

                st.markdown("#### Score breakdown")

                score_data = {
                    "Rule": scores.get("rule_score", 0),
                    "Semantic": scores.get("semantic_score", 0),
                    "Experience": scores.get("experience_score", 0),
                    "LLM fit": scores.get("llm_fit_score", 0),
                }

                st.bar_chart(
                    pd.DataFrame(
                        {
                            "Component score": score_data
                        }
                    )
                )

                st.markdown("#### Skills")
                st.write(
                    "**Matched:** "
                    + (
                        ", ".join(item.get("matched_skills", []))
                        or "None reported"
                    )
                )
                st.write(
                    "**Missing:** "
                    + (
                        ", ".join(item.get("missing_skills", []))
                        or "None reported"
                    )
                )

                st.markdown("#### Explanation")
                st.write(
                    item.get("explanation", "No explanation available.")
                )

                if item.get("llm_reason"):
                    st.caption(
                        "Fit-rating reason: " + item["llm_reason"]
                    )

                st.markdown("#### Evidence snippets")

                evidence = item.get("evidence_snippets", [])

                if evidence:
                    for snippet in evidence:
                        st.info(snippet)
                else:
                    st.write("No evidence snippets were returned.")

                for warning in item.get("warnings", []):
                    st.warning(warning)

    else:
        st.warning("No resumes were successfully screened.")

    if failures:
        st.markdown("### Files that could not be screened")

        st.dataframe(
            pd.DataFrame(failures),
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "Human review is required. Scores and extracted evidence can "
        "contain errors and must not be used as the sole basis for hiring."
    )
