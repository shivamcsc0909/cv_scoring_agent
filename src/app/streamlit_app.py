import streamlit as st
import os
from dotenv import load_dotenv
import openai

from app.parser import parse_resume
from app.scorer import score_resume_with_job_description, log_resume_score

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="CV Scoring AI", layout="wide")
st.title("📄 CV Scoring AI")
st.write("Upload your resume and optionally paste a job description.")

# Upload resume
uploaded = st.file_uploader("Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_input = st.text_area("Job Description (optional)")

if st.button("Score"):
    if not uploaded:
        st.error("Please upload a resume.")
    else:
        tmp = f"temp_{uploaded.name}"
        with open(tmp, "wb") as f:
            f.write(uploaded.getbuffer())

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
