import streamlit as st
from pathlib import Path

st.title("Resume Scoring Agent")

# Upload JD
jd_file = st.file_uploader("Upload Job Description", type=["txt", "pdf", "docx"])
# Upload Resume
resumes = st.file_uploader("Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

if st.button("Process"):
    st.success("Processing resumes...")
    # Save files, run analysis function
    for resume in resumes:
        path = Path("resumes") / resume.name
        with open(path, "wb") as f:
            f.write(resume.getbuffer())
    # Add your scoring logic here
    st.success("Done scoring resumes!")


from email_feedback import log_resume_score

from email_feedback import fetch_resumes
fetch_resumes()

import streamlit as st
import os

# Placeholder for score summary
st.title("Resume Scoring Summary")
st.write("Here are the scores for each uploaded resume:")

# Assuming you have a function log_resume_score() that logs the scores
# This will display score data from your log file
log_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "app.log")

if os.path.exists(log_file_path):
    with open(log_file_path, "r") as file:
        logs = file.readlines()
        for log in logs:
            st.write(log.strip())  # Display each log entry as a score summary
else:
    st.write("No score logs found.")
import streamlit as st
import os

# Placeholder for score summary
st.title("Resume Scoring Summary")
st.write("Here are the scores for each uploaded resume:")

# Assuming you have a function log_resume_score() that logs the scores
# This will display score data from your log file
log_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "app.log")

if os.path.exists(log_file_path):
    with open(log_file_path, "r") as file:
        logs = file.readlines()
        for log in logs:
            st.write(log.strip())  # Display each log entry as a score summary
else:
    st.write("No score logs found.")
import streamlit as st
import os

# Directory to save uploaded files
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def handle_file_upload(uploaded_files):
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.write(f"File {uploaded_file.name} saved.")
            return file_path
    return None

# Job description upload
st.subheader("Upload Job Description")
job_description_file = st.file_uploader("Upload Job Description (TXT, PDF, DOCX)", type=["txt", "pdf", "docx"])

if job_description_file:
    job_description_path = handle_file_upload([job_description_file])
    st.write(f"Job Description uploaded: {job_description_path}")

# Resume upload
st.subheader("Upload Resumes")
uploaded_files = st.file_uploader("Upload Resume(s) (PDF, DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if uploaded_files:
    resume_paths = [handle_file_upload([file]) for file in uploaded_files]
    st.write(f"{len(resume_paths)} Resumes uploaded successfully.")
<<<<<<< HEAD

import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from scorer import get_feedback
from ui_components import draw_score_chart

st.set_page_config(page_title="CV ScorePro", layout="wide")
st.title("🤖 CV ScorePro")

uploaded_files = st.file_uploader("Upload CVs (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
jd_input = st.text_area("Paste the Job Description", height=200)

if uploaded_files and jd_input:
    for file in uploaded_files:
        st.markdown(f"---\n### 📄 {file.name}")
        
        if file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file)
        else:
            resume_text = extract_text_from_docx(file)

        with st.spinner("Analyzing..."):
            result = get_feedback(resume_text, jd_input)

        try:
            score = int([s for s in result.split() if s.isdigit()][0])  # crude score fetch
        except:
            score = 60  # fallback

        st.plotly_chart(draw_score_chart(score), use_container_width=True)
        st.write("📝 **Feedback:**")
        st.markdown(result)
=======
>>>>>>> f9a190cb85d5e48e255119f15a634606055a8efd
