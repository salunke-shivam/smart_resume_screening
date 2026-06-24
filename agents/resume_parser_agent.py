import json
from gateway.llm_gateway import call_llm


SYSTEM_PROMPT = """You are a resume parser. Extract the following details from the resume text and return only a JSON object.
Fields to extract:
- name: full name of the candidate
- email: email address
- phone: phone number (if present)
- skills: a list of technical skills (languages, frameworks, tools)
- experience: a short summary of work experience (years, roles)
- education: degree, university, year
- projects: list of project titles or summaries
- certifications: list of certifications
- extra_activities: list of hackathons, open source contributions, etc.

If a field is missing, set it to empty string or empty list accordingly. Only return the JSON, nothing else."""


def parse_resume(resume_text):
    # extract structured data from resume text
    
    prompt = "Parse this resume and return the JSON:\n\n" + resume_text[:4000]
    
    reply = call_llm(prompt, system_prompt=SYSTEM_PROMPT)
    
    if reply is None:
        return {"error": "Failed to parse resume"}
    
    reply = reply.strip()
    
    # remove code fences if any
    if reply.startswith("```"):
        reply = reply.split("\n", 1)[1]
        if reply.endswith("```"):
            reply = reply[:-3]
        reply = reply.strip()
    
    try:
        data = json.loads(reply)
        return data
    except json.JSONDecodeError:
        return {"error": "Could not parse JSON from LLM response", "raw": reply}