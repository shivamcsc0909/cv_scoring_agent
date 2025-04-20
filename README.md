💼 CV Scoring Agent — AI-Powered Resume Evaluator
CV Scoring Agent is an intelligent tool that helps you automatically analyze and score resumes based on a given job description. It provides detailed feedback, category-wise breakdown, and a final score out of 100 — making hiring or self-evaluation smoother and smarter.

🔍 Features
📂 Upload multiple resumes (PDF, DOCX)

📝 Paste a custom job description

🧠 AI-generated feedback and suggestions

📊 Visual scoring and category-wise evaluation

🔐 Secure use of environment variables (API keys & email credentials)

🚀 Technologies Used
Python 3.10

Streamlit – Interactive web app

LangChain – AI-powered reasoning

OpenAI GPT API – For analyzing and generating feedback

IMAP/SMTP – For email resume handling

dotenv – For managing secrets

🛠️ How to Run the Project Locally
Follow these simple steps to get started on your machine:

📥 Step 1: Clone the Repository
git clone https://github.com/your-username/cv_scoring_agent.git
cd cv_scoring_agent


🧪 Step 2: Create Virtual Environment & Activate
Windows:

python -m venv venv
venv\Scripts\activate


📦 Step 3: Install Required Libraries

pip install -r requirements.txt


🔐 Step 4: Setup Environment Variables
Create a .env file in the root folder and paste the following:

OPENAI_API_KEY=your_openai_api_key

EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

IMAP_SERVER=imap.gmail.com
IMAP_PORT=993

RESUME_FOLDER=./resumes


📝 Use an App Password from Gmail for EMAIL_PASSWORD.

▶️ Step 5: Launch the App

streamlit run app/streamlit_ui.py
