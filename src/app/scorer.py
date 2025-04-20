<<<<<<< HEAD
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

# OpenAI Key for LangChain
openai_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0.3, openai_api_key=openai_key)

# Logging setup
logging.basicConfig(filename='logs/system.log', level=logging.INFO)

def log_resume_score(filename, score):
    logging.info(f"Parsed resume: {filename}, Score: {score}")


# -------------------------
# Scoring Functions
# -------------------------

def score_keywords(text, keyword_dict=KEYWORDS):
    score = 0
    matched_keywords = []
=======
# app/scorer.py
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from app.config import KEYWORDS, JD_KEYWORDS, SCORING_WEIGHTS

def score_keywords(text, keyword_dict=KEYWORDS):
    """कीवर्ड्स के आधार पर स्कोर करता है"""
    score = 0
    matched_keywords = []
    
>>>>>>> f9a190cb85d5e48e255119f15a634606055a8efd
    for category, words in keyword_dict.items():
        for keyword in words:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                score += 2
                matched_keywords.append(keyword)
                break
<<<<<<< HEAD
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
=======
    
    normalized_score = min(20, score)  # मैक्सिमम 20 तक
    return normalized_score, matched_keywords

def score_education(text):
    """एजुकेशन के आधार पर स्कोर करता है"""
    education_score = 0
    education_level = 0
    
    # डिग्री लेवल चेक करें
    if re.search(r'\b(ph\.?d|doctor|doctorate)\b', text, re.IGNORECASE):
        education_level = 4
    elif re.search(r'\b(masters|mba|m\.tech|m\.sc|m\.e|mca)\b', text, re.IGNORECASE):
        education_level = 3
    elif re.search(r'\b(bachelor|b\.tech|b\.e|bca|b\.sc|engineering)\b', text, re.IGNORECASE):
        education_level = 2
    elif re.search(r'\b(diploma|certificate|12th|intermediate)\b', text, re.IGNORECASE):
        education_level = 1
    
    # शैक्षिक संस्थानों की रैंकिंग या प्रसिद्धि
    prestigious = re.search(r'\b(iit|nit|bits|iisc|top|prestigious)\b', text, re.IGNORECASE)
    
    # स्कोर कैलकुलेट करें
    education_score = min(20, education_level * 5 + (5 if prestigious else 0))
    
    return education_score

def score_experience(text, years_experience):
    """Work experience के आधार पर स्कोर करता है"""
    # सालों के आधार पर बेसिक स्कोर
    if years_experience >= 5:
        experience_score = 20
    elif years_experience >= 3:
        experience_score = 15
    elif years_experience >= 1:
        experience_score = 10
    else:
        experience_score = 5
    
    # प्रोजेक्ट्स या इंटर्नशिप्स के लिए अतिरिक्त पॉइंट्स
    if re.search(r'\b(project|developed|created|built|designed|implemented)\b', text, re.IGNORECASE):
        experience_score = min(20, experience_score + 5)
    
    return experience_score

def score_skills(text):
    """Technical skills के आधार पर स्कोर करता है"""
    skill_score = 0
    skill_count = 0
    
    # प्रोग्रामिंग लैंग्वेजेज़
    langs = re.findall(r'\b(python|java|javascript|c\+\+|c#|php|ruby|go|rust|swift)\b', text, re.IGNORECASE)
    skill_count += len(set(langs))
    
    # फ्रेमवर्क्स
    frameworks = re.findall(r'\b(react|angular|vue|django|flask|spring|laravel|express|node\.js|tensorflow|pytorch)\b', text, re.IGNORECASE)
    skill_count += len(set(frameworks))
    
    # डेटाबेस
    db = re.findall(r'\b(sql|mysql|postgresql|mongodb|oracle|sqlite|nosql|redis)\b', text, re.IGNORECASE)
    skill_count += len(set(db))
    
    # टूल्स
    tools = re.findall(r'\b(git|docker|kubernetes|aws|azure|gcp|linux|ci/cd|jenkins|agile|scrum)\b', text, re.IGNORECASE)
    skill_count += len(set(tools))
    
    # स्किल स्कोर कैलकुलेट करें
    skill_score = min(20, skill_count * 2)
    
    return skill_score

def score_formatting(text):
    """रेज्यूमे फॉर्मेटिंग स्कोर करता है"""
    format_score = 10  # डिफॉल्ट स्कोर
    
    # लेंथ चेक
    if len(text) < 200:
        format_score -= 5
    elif len(text) > 10000:
        format_score -= 2
        
    # सेक्शन चेक
    sections = ["experience", "education", "skills", "projects", "objective", "summary"]
    section_count = sum(1 for section in sections if re.search(rf'\b{section}\b', text, re.IGNORECASE))
    
    if section_count >= 4:
        format_score += 5
    elif section_count >= 2:
        format_score += 2
        
    # बुलेट पॉइंट्स का उपयोग
    bullets = len(re.findall(r'•|\-|\*|\d+\.', text))
    if bullets > 10:
        format_score += 5
    elif bullets > 5:
        format_score += 3
        
    return min(20, max(0, format_score))

def score_jd_match(text, jd_keywords=JD_KEYWORDS):
    """जॉब डिस्क्रिप्शन मैच स्कोर करता है"""
    vectorizer = CountVectorizer(vocabulary=jd_keywords, lowercase=True)
    
    # टेक्स्ट को वेक्टर में कनवर्ट करें
    cv_vector = vectorizer.fit_transform([text.lower()])
    
    # कितने कीवर्ड्स मैच हुए
    matched_words = sum(1 for count in cv_vector.toarray()[0] if count > 0)
    total_keywords = len(jd_keywords)
    
    # स्कोर कैलकुलेट करें
    if total_keywords > 0:
        match_percentage = (matched_words / total_keywords) * 100
        jd_score = int((match_percentage / 100) * 20)
    else:
        jd_score = 0
        
    return min(20, jd_score)

def calculate_total_score(score_dict, weights=SCORING_WEIGHTS):
    """सभी स्कोर्स का वेटेड एवरेज निकालता है"""
    total = 0
    for category, score in score_dict.items():
        if category in weights:
            total += score * (weights[category] / 100)
    
    return round(total)

def score_resume(resume_data):
    """रेज्यूमे के लिए कॉम्प्रिहेंसिव स्कोरिंग करता है"""
    text = resume_data["text"]
    
    # अलग-अलग कैटेगरी स्कोरिंग
>>>>>>> f9a190cb85d5e48e255119f15a634606055a8efd
    keyword_score, matched_keywords = score_keywords(text)
    education_score = score_education(text)
    experience_score = score_experience(text, resume_data["years_experience"])
    skill_score = score_skills(text)
    format_score = score_formatting(text)
    jd_score = score_jd_match(text)
<<<<<<< HEAD

=======
    
    # स्कोर्स का डिक्शनरी
>>>>>>> f9a190cb85d5e48e255119f15a634606055a8efd
    scores = {
        "Education": education_score,
        "Experience": experience_score,
        "Skills": skill_score,
        "Formatting": format_score,
        "JD Match": jd_score
    }
<<<<<<< HEAD

    total_score = calculate_total_score(scores)

    strengths = [k for k, v in scores.items() if v >= 15]
    weaknesses = [k for k, v in scores.items() if v < 10]

    feedback = generate_feedback(scores, strengths, weaknesses, matched_keywords, total_score)

=======
    
    # टोटल स्कोर
    total_score = calculate_total_score(scores)
    
    # स्ट्रेंग्थ्स और वीकनेसेस
    strengths = []
    areas_to_improve = []
    
    for category, score in scores.items():
        if score >= 15:
            strengths.append(category)
        elif score < 10:
            areas_to_improve.append(category)
    
    # फीडबैक जनरेट करें
    feedback = generate_feedback(scores, strengths, areas_to_improve, matched_keywords, total_score)
    
>>>>>>> f9a190cb85d5e48e255119f15a634606055a8efd
    return {
        "scores": scores,
        "total_score": total_score,
        "strengths": strengths,
<<<<<<< HEAD
        "areas_to_improve": weaknesses,
        "feedback": feedback
    }


# GPT-based scoring from JD (optional)
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
=======
        "areas_to_improve": areas_to_improve,
        "feedback": feedback
    }

def generate_feedback(scores, strengths, areas_to_improve, matched_keywords, total_score):
    """स्कोर्स के आधार पर पर्सनलाइज्ड फीडबैक जनरेट करता है"""
    feedback = ""
    
    # स्ट्रेंग्थ्स पर फीडबैक
    if strengths:
        feedback += "Strengths:\n"
        for strength in strengths:
            if strength == "Education":
                feedback += "- Your educational background is relevant and well-presented.\n"
            elif strength == "Experience":
                feedback += "- Your work experience demonstrates relevant skills for this role.\n"
            elif strength == "Skills":
                feedback += "- You have a strong technical skill set matching our requirements.\n"
            elif strength == "Formatting":
                feedback += "- Your resume is well-structured and professional in presentation.\n"
            elif strength == "JD Match":
                feedback += "- Your profile is well-aligned with the job requirements.\n"
    
    # सुधार के क्षेत्रों पर फीडबैक
    if areas_to_improve:
        feedback += "\nAreas to Improve:\n"
        for area in areas_to_improve:
            if area == "Education":
                feedback += "- Consider highlighting your education more prominently or adding relevant courses/certifications.\n"
            elif area == "Experience":
                feedback += "- Try to provide more specific details about your roles and achievements.\n"
            elif area == "Skills":
                feedback += "- You could strengthen your technical skills section by adding more specific technologies.\n"
            elif area == "Formatting":
                feedback += "- Consider improving your resume format for better readability and structure.\n"
            elif area == "JD Match":
                feedback += "- Your resume could be better tailored to highlight skills relevant to the job description.\n"
    
    # जनरल रेकमेंडेशन
    feedback += "\nRecommendations:\n"
    if matched_keywords:
        feedback += f"- You've effectively included key terms like: {', '.join(matched_keywords[:5])}.\n"
    
    if total_score >= 75:
        feedback += "- Overall, your profile is strong. If you've included a cover letter, ensure it highlights your enthusiasm for this specific role.\n"
    elif total_score >= 50:
        feedback += "- Consider adding more specific achievements with measurable results to stand out from other candidates.\n"
    else:
        feedback += "- We recommend updating your resume to better highlight your qualifications that match the job requirements.\n"
    
    return feedback

from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file from the root

email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")
openai_key = os.getenv("OPENAI_API_KEY")


import logging

logging.basicConfig(filename='logs/system.log', level=logging.INFO)

def log_resume_score(filename, score):
    logging.info(f"Parsed resume: {filename}, Score: {score}")
>>>>>>> f9a190cb85d5e48e255119f15a634606055a8efd
