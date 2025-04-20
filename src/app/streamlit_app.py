import streamlit as st
from app.parser import parse_resume
from app.scorer import score_resume_with_job_description, log_resume_score

st.set_page_config(page_title="CV Scoring AI", layout="wide")

st.title("📄 CV Scoring AI")
st.write("Upload your resume and optionally paste a job description.")

uploaded = st.file_uploader("Resume (PDF/DOCX)", type=["pdf","docx"])
jd_input = st.text_area("Job Description (optional)")

if st.button("Score"):
    if not uploaded:
        st.error("Please upload a resume.")
    else:
        tmp = f"temp_{uploaded.name}"
        with open(tmp, "wb") as f: f.write(uploaded.getbuffer())
        data, err = parse_resume(tmp)
        os.remove(tmp)
        if err:
            st.error(err)
        else:
            if jd_input.strip():
                total, fb = score_resume_with_job_description(data['text'], jd_input)
            else:
                total, fb = score_resume_with_job_description(data['text'], "")
            st.success(f"Score: {total}/100")
            st.markdown(fb)
            log_resume_score(uploaded.name, total)
# app.py
import streamlit as st
from scorer import score_resume
from scorer import log_resume_score
from scorer import score_resume_with_job_description

st.set_page_config(page_title="CV Scoring AI", layout="wide")

st.title("📄 CV Scoring AI")
st.write("Upload your resume to get a detailed score and feedback. You can also paste a Job Description to get a match score.")

# Resume Upload
resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

# Job Description Input (optional)
job_description = st.text_area("Paste Job Description (Optional)", height=200)

if st.button("Score Resume"):
    if resume_file is None:
        st.warning("Please upload a resume first.")
    else:
        resume_bytes = resume_file.read()

        if job_description.strip():
            result = score_resume_with_job_description(resume_bytes, job_description)
        else:
            result = score_resume({"text": resume_bytes, "years_experience": 0})  # Add parser for experience if needed

        total = result.get("total_score", 0)
        feedback = result.get("feedback", "")
        scores = result.get("scores", {})

        st.subheader(f"Total Resume Score: {total}/100")
        st.progress(total)

        st.markdown("### Detailed Section Scores")
        for k, v in scores.items():
            st.write(f"- **{k}**: {v}/20")

        st.markdown("### Feedback")
        st.info(feedback)

        log_resume_score(resume_file.name, total)
 import streamlit as st
import os
from scorer import score_resume, scorer, parse_resume
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title('Resume Scoring App')

# File uploader widget
uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Parse the resume
    parsed_resume, error = parse_resume(file_path)
    os.remove(file_path)  # Clean up the temporary file

    if parsed_resume:
        st.subheader("Resume Information")
        st.write(f"Name: {parsed_resume['name']}")
        st.write(f"Email: {parsed_resume['email']}")
        st.write(f"Phone: {parsed_resume['phone']}")
        st.write(f"Years of Experience: {parsed_resume['years_experience']}")

        # Score the resume (using the existing `scorer` or `score_resume` function)
        job_description = "Job description or specific role here"  # Or let users input a job description
        score = score_resume(parsed_resume["text"], job_description)
        st.subheader("Resume Score")
        st.write(f"Score: {score}")

    else:
        st.error(f"Error: {error}")
