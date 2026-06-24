import os
from dotenv import load_dotenv

load_dotenv()

# groq settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama3-70b-8192")
GROQ_TEMPERATURE = 0.1
GROQ_MAX_TOKENS = 4096

# rag settings
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME_JD = "job_descriptions"
COLLECTION_NAME_RESUME = "resumes"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# how many results to get from search
SEMANTIC_TOP_K = 5
KEYWORD_TOP_K = 5

# hybrid search weights
SEMANTIC_WEIGHT = 0.6
KEYWORD_WEIGHT = 0.4

# memory settings
MAX_MEMORY_TOKENS = 2000

# fresher job scoring weights
FRESHER_WEIGHTS = {
    "technical_skills": 0.35,
    "academic_projects": 0.25,
    "education": 0.20,
    "certifications": 0.15,
    "extra_activities": 0.05
}

# experienced job scoring weights
EXPERIENCED_WEIGHTS = {
    "technical_skills": 0.35,
    "work_experience": 0.25,
    "education": 0.15,
    "project_relevance": 0.15,
    "certifications": 0.10
}

# internship job scoring weights
INTERNSHIP_WEIGHTS = {
    "technical_skills": 0.30,
    "academic_projects": 0.25,
    "education": 0.20,
    "certifications": 0.15,
    "extra_activities": 0.10
}

# keywords to find out what type of job it is
FRESHER_KEYWORDS = [
    "fresher",
    "fresh graduate",
    "entry level",
    "0-1 years",
    "0 years",
    "no experience required",
    "trainee",
    "junior"
]

EXPERIENCED_KEYWORDS = [
    "2+ years",
    "3+ years",
    "5+ years",
    "senior",
    "lead",
    "manager",
    "minimum experience",
    "experienced"
]

INTERNSHIP_KEYWORDS = [
    "internship",
    "intern",
    "6 months",
    "part time",
    "temporary"
]

# azure settings
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "resumes")
AZURE_KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")
AZURE_MONITOR_CONNECTION_STRING = os.getenv("AZURE_MONITOR_CONNECTION_STRING")

# email settings
#SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Smart Resume Screener")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# database
DATABASE_URL = os.getenv("DATABASE_URL")

# langsmith monitoring
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "smart-resume-screener")

# app settings
APP_ENV = os.getenv("APP_ENV", "development")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# file upload settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = [".pdf", ".docx"]
MAX_RESUMES_PER_SESSION = 50

# screening settings
TOP_CANDIDATES_TO_INVITE = 3
MIN_SCORE_FOR_INVITE = 60.0