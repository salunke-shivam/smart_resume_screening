# 🧠 Smart Resume Screener

An intelligent, agentic AI system that scans resumes, matches them to a job description, and automatically sends interview invites – all built with **Python**, **LangChain**, **Groq**, and **Azure**.

---

## 📌 What does this project do?

Imagine you are an HR person with a stack of 100 resumes. This tool:

1. Reads a job description (PDF/DOCX)
2. Analyses it to understand required skills, experience, and job type (fresher / experienced / internship)
3. Reads all resumes (PDF/DOCX) and extracts candidate details
4. Uses a hybrid search (semantic + keyword) to match every resume to the JD
5. Scores and ranks all candidates fairly – using different weightage for freshers, experienced, and interns
6. Sends interview invites (via email) to the top N candidates, and polite rejections to the rest
7. Generates a screening report
8. Logs everything for monitoring

You can use it with a simple web dashboard built in Streamlit.

---

## 🏗️ Architecture (Simple Overview)

Recruiter opens Dashboard
        ↓
Creates a Session
        ↓
Pastes Job Description → AI extracts skills & detects job type
        ↓
Uploads Resumes (PDF/DOCX) → AI extracts name, skills, education, projects
        ↓
Hybrid RAG matches JD + Resumes (meaning + exact keywords)
        ↓
Scoring Agent applies correct weights → Calculates 0-100 score
        ↓
Guardrails validate results → Session memory stores ranking
        ↓
HR sets threshold → System filters & ranks candidates
        ↓
Email Agent sends invites/rejections → Dashboard shows results


All the “thinking” is done by AI agents that call **Groq’s fast LLM** (LLaMA 3) under the hood.

---

## ✨ Features

- ✅ Upload job description and resumes (PDF / DOCX)
- ✅ Automatic job type detection (fresher / experienced / internship)
- ✅ Dynamic scoring – freshers are not penalised for lack of experience
- ✅ Hybrid search: understands meaning, not just exact keywords
- ✅ Guardrails to block biased or harmful content
- ✅ Sends personalised interview invites and rejections
- ✅ Dashboard with live ranking, adjustable invite count, and score threshold
- ✅ Monitoring with LangSmith
- ✅ Docker support for easy sharing
- ✅ Fully local – runs on your laptop

---

## 🛠️ Technologies Used

| Layer               | Technology                        |
|---------------------|-----------------------------------|
| Frontend            | Streamlit                         |
| Backend API         | FastAPI                           |
| AI Brain            | LangChain + Groq (LLaMA 3.3)     |
| Vector Search       | ChromaDB + Sentence Transformers  |
| Keyword Search      | BM25 (NLTK)                       |
| Guardrails          | Custom validation via LLM         |
| Email               | Gmail SMTP (or SendGrid)          |
| Storage             | Azure Blob Storage                |
| Monitoring          | LangSmith                         |
| Containerisation    | Docker                            |
---

## 🚀 How to Run this Project on Your Machine

### 1️⃣ Prerequisites

- Python 3.11 (or 3.10/3.12)
- A Gmail account (for sending emails)
- [Optional] Docker Desktop (if you want to use Docker)

---

### 2️⃣ Get API Keys

You need these free keys:

- **Groq API Key** – Go to [console.groq.com](https://console.groq.com), sign up, create a key.
- **LangSmith API Key** – Go to [smith.langchain.com](https://smith.langchain.com), sign up, create a key. (Optional but recommended to see AI trace)
- **Azure Storage Connection String** – If you want files saved to cloud. Use the free Azure student account: create a Storage Account → copy connection string.

Don’t worry if you can’t get the Azure key right away – the project still works without it (you just won’t save files to the cloud).

---

### 3️⃣ Create your `.env` file

Copy the provided `.env.example` (or create a new file), rename it to `.env`, and fill in your keys. It should look like:


GROQ_API_KEY=gsk_xxxx
GROQ_MODEL_NAME=llama-3.1-8b-instant

LANGCHAIN_API_KEY=ls__xxxx
LANGCHAIN_PROJECT=smart-resume-screener

AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;...
AZURE_CONTAINER_NAME=resumes

EMAIL_FROM=your_email@gmail.com
GMAIL_APP_PASSWORD=xxxx # 16-char app password (see next step)


---

### 4️⃣ Generate a Gmail App Password

1. Go to your Google Account → **Security**
2. Enable **2‑Step Verification** if not already on
3. Then create an **App Password**: choose *Mail* and *Other (Resume Screener)*
4. Copy the 16‑character password into `GMAIL_APP_PASSWORD`

---

### 5️⃣ Install Python packages

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt

tart the project
Terminal 1 – Start the backend:

Bash

uvicorn api.main:app --reload
You should see: Uvicorn running on http://0.0.0.0:8000

Terminal 2 – Start the frontend:

Bash

streamlit run frontend/dashboard.py
A browser tab will open at http://localhost:8501. That’s your dashboard.

🐳 (Optional) Run with Docker
Bash

docker build -t smart-resume-screener -f deployment/Dockerfile .
docker run -p 8000:8000 --env-file .env -v ./chroma_db:/app/chroma_db smart-resume-screener
Then run the Streamlit frontend normally.

🧪 How to Use the Dashboard
Upload JD – select a PDF/DOCX job description. Click “Upload JD”. The system will tell you the job type.
Upload Resumes – select multiple resume files. Click “Upload Resumes”. Each resume will be parsed.
Screen – click “Start Screening”. You’ll see a ranking with scores.
Send Emails – set “Number of top candidates” and “Minimum score”. Click “Send Emails”. Invites go to the top N candidates above the threshold; others get rejection emails.
View Report – generates a text summary.
📊 How Scoring Works
The scoring is dynamic – it detects whether the job is for freshers, experienced, or interns and applies different weightage:

Parameter	Fresher %	Experienced %	Internship %
RAG similarity	70	60	65
Direct skills match	20	25	20
Education	5	5	10
Projects relevance	5	10	5
This means freshers are not penalised for lack of work experience – the emphasis is on their skills and projects.

🔍 Troubleshooting
Problem	Solution
groq.RateLimitError	Switch to a smaller model in .env (llama-3.1-8b-instant) or wait a few minutes.
python-dotenv could not parse	Check your .env file – no # inside values, each line is KEY=VALUE.
BadRequestError: model decommissioned	Change GROQ_MODEL_NAME to llama-3.3-70b-versatile or llama-3.1-8b-instant.
Email error (Username and Password not accepted)	You must use an App Password, not your normal Gmail password.
ChromaDB metadata error	Ensure you ran the updated code – parsed data is converted to a string before storing.
Dashboard shows “Error: Status 500”	Check the backend terminal for the exact error. Most often a missing key in .env.
🤝 Contributing
If you want to improve this project:

Fork this repository
Create a new branch (git checkout -b feature/your-feature)
Commit your changes
Push to the branch
Open a Pull Request
📜 License
This project is for educational and portfolio purposes. Feel free to use it for learning or as a base for your own job-screening tool.

🙋‍♂️ Still stuck?
Reach out or open an issue – I’ll be happy to help you run it.

Built with ❤️ using Python, Groq, and LangChain.
