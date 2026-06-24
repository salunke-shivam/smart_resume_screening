import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Smart Resume Screener", layout="wide")
st.title("Smart Resume Screener")
st.write("Upload a job description, resumes, and screen candidates intelligently.")

# sidebar
st.sidebar.title("Actions")
action = st.sidebar.radio("Choose action", ["Upload JD", "Upload Resumes", "Screen", "Send Emails", "View Report"])

# ---- Upload JD ----
if action == "Upload JD":
    st.header("Upload Job Description")
    jd_file = st.file_uploader("Choose a file", type=["pdf", "docx"], key="jd")
    if jd_file is not None:
        if st.button("Upload JD"):
            with st.spinner("Uploading and analyzing..."):
                files = {"file": (jd_file.name, jd_file.getvalue())}
                resp = requests.post(f"{API_URL}/upload-jd", files=files)

                data = None
                try:
                    data = resp.json()
                except Exception:
                    pass

                if resp.status_code == 200 and data:
                    st.success("Job description uploaded and analyzed!")
                    st.json(data.get("analysis", {}))
                    st.info(f"Job Type: {data.get('job_type', 'unknown')}")
                else:
                    err = "Unknown error"
                    if data and isinstance(data, dict):
                        err = data.get("error", err)
                    else:
                        err = resp.text[:200] if resp.text else f"Status {resp.status_code}"
                    st.error(f"Error: {err}")

# ---- Upload Resumes ----
elif action == "Upload Resumes":
    st.header("Upload Resumes")
    resume_files = st.file_uploader("Choose resume files", type=["pdf", "docx"], accept_multiple_files=True, key="resumes")
    if resume_files:
        st.write(f"Selected {len(resume_files)} files")
        if st.button("Upload Resumes"):
            with st.spinner("Uploading and parsing..."):
                files = [("files", (f.name, f.getvalue())) for f in resume_files]
                resp = requests.post(f"{API_URL}/upload-resumes", files=files)

                data = None
                try:
                    data = resp.json()
                except Exception:
                    pass

                if resp.status_code == 200 and data:
                    st.success(f"Uploaded {data.get('uploaded', 0)} resumes")
                    for result in data.get("results", []):
                        if "error" in result:
                            st.warning(f"{result['filename']}: {result['error']}")
                        else:
                            name = result.get("parsed", {}).get("name", "Unknown")
                            st.write(f"✅ {result['filename']} - Name: {name}")
                else:
                    err = "Unknown error"
                    if data and isinstance(data, dict):
                        err = data.get("error", err)
                    else:
                        err = resp.text[:200] if resp.text else f"Status {resp.status_code}"
                    st.error(f"Error: {err}")

# ---- Screen ----
elif action == "Screen":
    st.header("Screen Candidates")
    st.write("Score and rank all uploaded candidates against the job description.")
    if st.button("Start Screening"):
        with st.spinner("Screening..."):
            resp = requests.post(f"{API_URL}/screen")

            data = None
            try:
                data = resp.json()
            except Exception:
                pass

            if resp.status_code == 200 and data:
                st.success("Screening completed!")
                ranking = data.get("ranking", [])
                if ranking:
                    st.subheader("Ranking")
                    for cand in ranking:
                        name = cand.get("parsed", {}).get("name", "Unknown")
                        st.write(f"**Rank {cand['rank']}** - Score: {cand['score']} - {name}")
                else:
                    st.info("No candidates to screen.")
            else:
                err = "Unknown error"
                if data and isinstance(data, dict):
                    err = data.get("error", err)
                else:
                    err = resp.text[:200] if resp.text else f"Status {resp.status_code}"
                st.error(f"Error: {err}")

# ---- Send Emails ----
elif action == "Send Emails":
    st.header("Send Emails")
    st.write("Send interview invites to top candidates and rejections to others.")

    # HR settings – top N and minimum score
    num_invites = st.number_input("Number of top candidates to invite", min_value=1,
                                  value=3, step=1)
    min_score_threshold = st.slider("Minimum score to receive invite", min_value=0.0,
                                    max_value=100.0, value=60.0, step=5.0)

    if st.button("Send Emails"):
        with st.spinner("Sending emails..."):
            resp = requests.post(
                f"{API_URL}/send-emails?top_n={num_invites}&min_score={min_score_threshold}"
            )

            data = None
            try:
                data = resp.json()
            except Exception:
                pass

            if resp.status_code == 200 and data:
                st.success(f"Sent {data.get('sent', 0)} emails")
                for result in data.get("results", []):
                    name = result.get("name", "Candidate")
                    st.write(f"{name}: {result['status']}")
            else:
                err = "Unknown error"
                if data and isinstance(data, dict):
                    err = data.get("error", err)
                else:
                    err = resp.text[:200] if resp.text else f"Status {resp.status_code}"
                st.error(f"Error: {err}")

# ---- View Report ----
elif action == "View Report":
    st.header("Screening Report")
    if st.button("Generate Report"):
        with st.spinner("Generating..."):
            resp = requests.get(f"{API_URL}/report")

            data = None
            try:
                data = resp.json()
            except Exception:
                pass

            if resp.status_code == 200 and data:
                report = data.get("report", "No report available")
                st.text(report)
            else:
                err = "Unknown error"
                if data and isinstance(data, dict):
                    err = data.get("error", err)
                else:
                    err = resp.text[:200] if resp.text else f"Status {resp.status_code}"
                st.error(f"Error: {err}")