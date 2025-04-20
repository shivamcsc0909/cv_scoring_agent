import re
import logging
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.config import KEYWORDS, JD_KEYWORDS, SCORING_WEIGHTS

# Load environment variables
load_dotenv()

# Configure LLM
openai_key = load_dotenv() or None
llm = ChatOpenAI(temperature=0.3, openai_api_key=openai_key)

# Logging setup
typedef = 'system.log'
logging.basicConfig(filename=f'logs/{typedef}', level=logging.INFO)

def log_resume_score(filename, score):
    logging.info(f"Parsed resume: {filename}, Score: {score}")


def score_keywords(text, keyword_dict=KEYWORDS):
    score = 0
    matched = []
    for _, words in keyword_dict.items():
        for kw in words:
            if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                score += 2
                matched.append(kw)
                break
    return min(20, score), matched


def score_education(text):
    level = 0
    if re.search(r"\b(ph\.\?d|doctor)\b", text, re.IGNORECASE): level = 4
    elif re.search(r"\b(masters|mba)\b", text, re.IGNORECASE): level = 3
    elif re.search(r"\b(bachelor)\b", text, re.IGNORECASE): level = 2
    elif re.search(r"\b(diploma|certificate)\b", text, re.IGNORECASE): level = 1
    prestige = bool(re.search(r"\b(iit|nit|bits)\b", text, re.IGNORECASE))
    return min(20, level*5 + (5 if prestige else 0))


def score_experience(text, years_experience):
    base = 20 if years_experience>=5 else 15 if years_experience>=3 else 10 if years_experience>=1 else 5
    bonus = 5 if re.search(r"\b(project|built|designed)\b", text, re.IGNORECASE) else 0
    return min(20, base + bonus)


def score_skills(text):
    patterns = [
        r"\b(python|java|c\+\+|javascript)\b",
        r"\b(react|django|flask)\b",
        r"\b(mysql|mongodb|sql)\b",
        r"\b(docker|aws|gcp)\b"
    ]
    count = sum(len(set(re.findall(p, text, re.IGNORECASE))) for p in patterns)
    return min(20, count*2)


def score_formatting(text):
    score = 10
    if len(text)<200: score -=5
    elif len(text)>10000: score -=2
    sections = sum(bool(re.search(rf"\b{s}\b",text,re.IGNORECASE)) for s in ["experience","education","skills","projects"])
    score += 5 if sections>=4 else 2 if sections>=2 else 0
    bullets = len(re.findall(r"\-|•|\*|\d+\.", text))
    score += 5 if bullets>10 else 3 if bullets>5 else 0
    return min(20, max(0, score))


def score_jd_match(text, jd_keywords=JD_KEYWORDS):
    vec = CountVectorizer(vocabulary=jd_keywords)
    arr = vec.fit_transform([text.lower()]).toarray()[0]
    matched = sum(1 for c in arr if c>0)
    return int((matched/len(jd_keywords))*20) if jd_keywords else 0


def calculate_total_score(scores, weights=SCORING_WEIGHTS):
    return round(sum(v*(weights.get(k,0)/100) for k,v in scores.items()))


def generate_feedback(scores, strengths, weaknesses, matched, total):
    fb = ""
    if strengths:
        fb += "**Strengths:**\n" + "\n".join(f"- {s}" for s in strengths) + "\n"
    if weaknesses:
        fb += "**Areas to Improve:**\n" + "\n".join(f"- {w}" for w in weaknesses) + "\n"
    fb += "**Recommendations:**\n"
    if matched: fb += f"- Keywords: {', '.join(matched[:5])}\n"
    fb += "- Great work!" if total>=75 else "- Keep refining your resume."
    return fb


def score_resume_with_job_description(resume_text, jd_text):
    # text version
    kw_score, matched = score_keywords(resume_text)
    edu = score_education(resume_text)
    exp = score_experience(resume_text, 0)
    skl = score_skills(resume_text)
    fmt = score_formatting(resume_text)
    jd = score_jd_match(jd_text)
    scores = {"Education":edu,"Experience":exp,"Skills":skl,"Formatting":fmt,"JD Match":jd}
    total = calculate_total_score(scores)
    strengths = [k for k,v in scores.items() if v>=15]
    weaknesses = [k for k,v in scores.items() if v<10]
    feedback = generate_feedback(scores, strengths, weaknesses, matched, total)

import re
import os
import logging
import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.config import KEYWORDS, JD_KEYWORDS, SCORING_WEIGHTS

# Load environment variables
load_dotenv()

# Email config (optional)
email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")
openai_key = os.getenv("OPENAI_API_KEY")

# LLM
llm = ChatOpenAI(temperature=0.3, openai_api_key=openai_key)

# Logging setup
logging.basicConfig(filename='logs/system.log', level=logging.INFO)

def log_resume_score(filename, score):
    logging.info(f"Parsed resume: {filename}, Score: {score}")

def score_keywords(text, keyword_dict=KEYWORDS):
    score = 0
    matched_keywords = []
    for category, words in keyword_dict.items():
        for keyword in words:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                score += 2
                matched_keywords.append(keyword)
                break
    return min(20, score), matched_keywords

def score_education(text):
    level = 0
    if re.search(r'\b(ph\.?d|doctor|doctorate)\b', text, re.IGNORECASE):
        level = 4
    elif re.search(r'\b(masters|mba|m\.tech|m\.sc|m\.e|mca)\b', text, re.IGNORECASE):
        level = 3
    elif re.search(r'\b(bachelor|b\.tech|b\.e|bca|b\.sc|engineering)\b', text, re.IGNORECASE):
        level = 2
    elif re.search(r'\b(diploma|certificate|12th|intermediate)\b', text, re.IGNORECASE):
        level = 1
    prestige = re.search(r'\b(iit|nit|bits|iisc|top|prestigious)\b', text, re.IGNORECASE)
    return min(20, level * 5 + (5 if prestige else 0))

def score_experience(text, years_experience):
    if years_experience >= 5:
        score = 20
    elif years_experience >= 3:
        score = 15
    elif years_experience >= 1:
        score = 10
    else:
        score = 5
    if re.search(r'\b(project|developed|created|built|designed|implemented)\b', text, re.IGNORECASE):
        score = min(20, score + 5)
    return score

def score_skills(text):
    skill_count = 0
    skill_count += len(set(re.findall(r'\b(python|java|javascript|c\+\+|c#|php|ruby|go|rust|swift)\b', text, re.IGNORECASE)))
    skill_count += len(set(re.findall(r'\b(react|angular|vue|django|flask|spring|laravel|express|node\.js|tensorflow|pytorch)\b', text, re.IGNORECASE)))
    skill_count += len(set(re.findall(r'\b(sql|mysql|postgresql|mongodb|oracle|sqlite|nosql|redis)\b', text, re.IGNORECASE)))
    skill_count += len(set(re.findall(r'\b(git|docker|kubernetes|aws|azure|gcp|linux|ci/cd|jenkins|agile|scrum)\b', text, re.IGNORECASE)))
    return min(20, skill_count * 2)

def score_formatting(text):
    score = 10
    if len(text) < 200:
        score -= 5
    elif len(text) > 10000:
        score -= 2
    sections = ["experience", "education", "skills", "projects", "objective", "summary"]
    section_count = sum(1 for section in sections if re.search(rf'\b{section}\b', text, re.IGNORECASE))
    score += 5 if section_count >= 4 else 2 if section_count >= 2 else 0
    bullets = len(re.findall(r'•|\-|\*|\d+\.', text))
    score += 5 if bullets > 10 else 3 if bullets > 5 else 0
    return min(20, max(0, score))

def score_jd_match(text, jd_keywords=JD_KEYWORDS):
    vectorizer = CountVectorizer(vocabulary=jd_keywords, lowercase=True)
    vector = vectorizer.fit_transform([text.lower()])
    matched_words = sum(1 for count in vector.toarray()[0] if count > 0)
    match_percent = (matched_words / len(jd_keywords)) * 100 if jd_keywords else 0
    return int((match_percent / 100) * 20)

def calculate_total_score(score_dict, weights=SCORING_WEIGHTS):
    return round(sum(score * (weights[cat] / 100) for cat, score in score_dict.items() if cat in weights))

def generate_feedback(scores, strengths, weaknesses, matched_keywords, total_score):
    feedback = ""
    if strengths:
        feedback += "Strengths:\n"
        for s in strengths:
            feedback += f"- Your {s.lower()} section is strong.\n"
    if weaknesses:
        feedback += "\nAreas to Improve:\n"
        for w in weaknesses:
            feedback += f"- Improve your {w.lower()} section with more relevant content.\n"
    feedback += "\nRecommendations:\n"
    if matched_keywords:
        feedback += f"- Good use of keywords: {', '.join(matched_keywords[:5])}\n"
    if total_score >= 75:
        feedback += "- Great profile! Consider attaching a focused cover letter.\n"
    elif total_score >= 50:
        feedback += "- Add more measurable achievements to stand out.\n"
    else:
        feedback += "- Revise your resume to better align with the job description.\n"
    return feedback

def score_resume(resume_data):
    text = resume_data["text"]
    keyword_score, matched_keywords = score_keywords(text)
    education_score = score_education(text)
    experience_score = score_experience(text, resume_data["years_experience"])
    skill_score = score_skills(text)
    format_score = score_formatting(text)
    jd_score = score_jd_match(text)

    scores = {
        "Education": education_score,
        "Experience": experience_score,
        "Skills": skill_score,
        "Formatting": format_score,
        "JD Match": jd_score
    }

    total_score = calculate_total_score(scores)
    strengths = [k for k, v in scores.items() if v >= 15]
    weaknesses = [k for k, v in scores.items() if v < 10]
    feedback = generate_feedback(scores, strengths, weaknesses, matched_keywords, total_score)

    return {
        "scores": scores,
        "total_score": total_score,
        "strengths": strengths,
        "areas_to_improve": weaknesses,
        "feedback": feedback
    }

def get_feedback(resume_text, jd_text):
    prompt = PromptTemplate.from_template("""
    You are a CV screening expert. Based on this JD:

    {jd}

    Evaluate this resume:

    {resume}

    Give a score out of 100 and explain in 3 bullet points.
    """)
    input_text = prompt.format(jd=jd_text, resume=resume_text)
    return llm.predict(input_text)
