import json
from gateway.llm_gateway import call_llm
import config


SYSTEM_PROMPT = """You are a job description analyzer. Extract the following details from the job description and return only a JSON object.
Fields to extract:
- role: job title
- required_skills: list of must-have skills
- good_to_have_skills: list of nice-to-have skills
- experience_years: number of years required (if mentioned)
- education: minimum degree required
- responsibilities: list of key responsibilities
- company_info: brief about the company

If a field is missing, set it to empty string or empty list. Only return the JSON, nothing else."""


def get_job_type(jd_text):
    # detect job type from keywords in config

    jd_lower = jd_text.lower()

    for word in config.FRESHER_KEYWORDS:
        if word in jd_lower:
            return "fresher"

    for word in config.INTERNSHIP_KEYWORDS:
        if word in jd_lower:
            return "internship"

    for word in config.EXPERIENCED_KEYWORDS:
        if word in jd_lower:
            return "experienced"

    # default to experienced
    return "experienced"


def analyze_jd(jd_text):
    # extract requirements and job type from JD

    prompt = "Analyze this job description and return the JSON:\n\n" + jd_text[:4000]

    reply = call_llm(prompt, system_prompt=SYSTEM_PROMPT)

    if reply is None:
        return {"error": "Failed to analyze JD"}

    reply = reply.strip()

    # remove code fences
    if reply.startswith("```"):
        reply = reply.split("\n", 1)[1]
        if reply.endswith("```"):
            reply = reply[:-3]
        reply = reply.strip()

    try:
        data = json.loads(reply)
    except json.JSONDecodeError:
        data = {"error": "Could not parse JSON", "raw": reply}

    # add job type
    data["job_type"] = get_job_type(jd_text)

    return data