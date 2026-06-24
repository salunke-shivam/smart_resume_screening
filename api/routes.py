from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
import os
import uuid
import json 

from monitoring.logger import log_info, log_error, log_agent_action
from guardrails.guardrails_manager import validate_input, validate_output
from agents.resume_parser_agent import parse_resume
from agents.jd_analyzer_agent import analyze_jd
from agents.scoring_agent import rank_candidates
from agents.email_agent import send_interview_invite, send_rejection
from agents.report_agent import generate_report
from memory.session_memory import memory
from rag.vector_store import add_resume, add_job_description
import config

router = APIRouter()


def _read_text_from_file(file: UploadFile):
    # read text from pdf or docx
    content = file.file.read()
    file.file.seek(0)  # reset for next read if needed

    ext = os.path.splitext(file.filename)[1].lower()

    if ext == ".pdf":
        try:
            import pdfplumber
            with pdfplumber.open(file.file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if not text.strip():
                raise ValueError("Empty PDF")
            return text
        except Exception as e:
            # fallback to pypdf
            try:
                from pypdf import PdfReader
                reader = PdfReader(file.file)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
            except Exception as e2:
                return ""
    elif ext == ".docx":
        try:
            from docx import Document
            doc = Document(file.file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception:
            return ""
    else:
        return content.decode("utf-8", errors="ignore")


@router.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)):
    # upload and analyze job description

    # check extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in config.ALLOWED_EXTENSIONS:
        return JSONResponse(status_code=400, content={"error": "File type not allowed"})

    # check size
    content = file.file.read()
    file.file.seek(0)
    size_mb = len(content) / (1024 * 1024)
    if size_mb > config.MAX_FILE_SIZE_MB:
        return JSONResponse(status_code=400, content={"error": "File too large"})

    # read text
    text = _read_text_from_file(file)
    if not text.strip():
        return JSONResponse(status_code=400, content={"error": "Could not read text from file"})

    # validate using guardrails
    is_valid, msg = validate_input(text, doc_type="jd")
    if not is_valid:
        return JSONResponse(status_code=400, content={"error": msg})

    # analyze
    log_agent_action("JD Analyzer", "start")
    analysis = analyze_jd(text)
    log_agent_action("JD Analyzer", "done", f"job_type={analysis.get('job_type')}")

    if "error" in analysis:
        return JSONResponse(status_code=500, content={"error": analysis["error"]})

    # store in memory
    memory.save_job_description(text)

    # store in vector db
    jd_id = str(uuid.uuid4())
    add_job_description(jd_id, text, {"job_type": analysis.get("job_type")})

    return JSONResponse(content={
        "message": "JD uploaded and analyzed",
        "analysis": analysis,
        "job_type": analysis.get("job_type"),
        "jd_id": jd_id
    })


@router.post("/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    # upload multiple resumes

    if len(files) > config.MAX_RESUMES_PER_SESSION:
        return JSONResponse(status_code=400, content={"error": "Too many resumes"})

    results = []

    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in config.ALLOWED_EXTENSIONS:
            results.append({"filename": file.filename, "error": "File type not allowed"})
            continue

        content = file.file.read()
        size_mb = len(content) / (1024 * 1024)
        if size_mb > config.MAX_FILE_SIZE_MB:
            results.append({"filename": file.filename, "error": "File too large"})
            continue

        text = _read_text_from_file(file)
        if not text.strip():
            results.append({"filename": file.filename, "error": "Could not read file"})
            continue

        # validate
        is_valid, msg = validate_input(text, doc_type="resume")
        if not is_valid:
            results.append({"filename": file.filename, "error": msg})
            continue

        # parse resume
        log_agent_action("Resume Parser", "start", f"file={file.filename}")
        parsed = parse_resume(text)
        if "error" in parsed:
            results.append({"filename": file.filename, "error": parsed["error"]})
            continue

        resume_id = str(uuid.uuid4())
        memory.add_resume(resume_id, text, {"filename": file.filename})
        add_resume(resume_id, text, {"filename": file.filename, "parsed": json.dumps(parsed)})
        results.append({
            "filename": file.filename,
            "resume_id": resume_id,
            "parsed": parsed
        })

    return JSONResponse(content={"uploaded": len(results), "results": results})


@router.post("/screen")
async def screen_candidates():
    # run scoring and ranking on uploaded resumes

    jd_text = memory.get_job_description()
    if not jd_text:
        return JSONResponse(status_code=400, content={"error": "No job description uploaded"})

    resumes = memory.get_all_resumes()
    if not resumes:
        return JSONResponse(status_code=400, content={"error": "No resumes uploaded"})

    # analyze jd again to get structured data
    jd_analysis = analyze_jd(jd_text)
    if "error" in jd_analysis:
        return JSONResponse(status_code=500, content={"error": "Failed to analyze JD"})

    # build candidates list for scoring
    candidates_list = []
    for r in resumes:
        # re-parse resume to get structured data
        parsed = parse_resume(r["text"])
        candidates_list.append({
            "resume_id": r["id"],
            "resume_text": r["text"],
            "parsed": parsed,
            "jd_text": jd_text,
            "jd_analysis": jd_analysis
        })

    log_agent_action("Scoring Agent", "start", f"candidates={len(candidates_list)}")
    ranking = rank_candidates(candidates_list)
    log_agent_action("Scoring Agent", "done")

    # store scores and ranking in memory
    scores_dict = {c["resume_id"]: c["score"] for c in ranking}
    memory.set_scores(scores_dict)
    ranked_ids = [c["resume_id"] for c in ranking]
    memory.set_ranking(ranked_ids)

    # generate report
    report = generate_report(ranking, jd_text, jd_analysis.get("job_type", "experienced"))

    return JSONResponse(content={
        "ranking": ranking,
        "report": report
    })


@router.post("/send-emails")
async def send_emails(top_n: int = None):
    # send invites to top candidates and rejections to others
    ranking = memory.ranking
    if not ranking:
        return JSONResponse(status_code=400, content={"error": "No screening results found"})

    resumes = {r["id"]: r for r in memory.get_all_resumes()}
    jd_analysis = analyze_jd(memory.get_job_description())
    company = jd_analysis.get("company_info", "Our Company")

    email_results = []

    top_n = config.TOP_CANDIDATES_TO_INVITE
    invite_count = 0
    if top_n is None:
        top_n = config.TOP_CANDIDATES_TO_INVITE
    if min_score is None:
        min_score = config.MIN_SCORE_FOR_INVITE
    # iterate in ranking order
    for rank_idx, resume_id in enumerate(ranking):
        resume_info = resumes.get(resume_id)
        if not resume_info:
            continue

        # parse to get name and email
        parsed = parse_resume(resume_info["text"])
        cand_name = parsed.get("name", "Candidate")
        cand_email = parsed.get("email", "")
        if not cand_email:
            email_results.append({"resume_id": resume_id, "name": cand_name, "status": "no email"})
            continue

        # top N get invites if above min score
        score = memory.scores.get(resume_id, 0)
        if invite_count < top_n and score >= config.MIN_SCORE_FOR_INVITE:
            success, detail = send_interview_invite(cand_name, cand_email, company)
            if success:
                email_results.append({"resume_id": resume_id, "name": cand_name, "status": "invited"})
                invite_count += 1
            else:
                email_results.append({"resume_id": resume_id, "name": cand_name, "status": f"failed: {detail}"})
        else:
            success, detail = send_rejection(cand_name, cand_email, company)
            if success:
                email_results.append({"resume_id": resume_id, "name": cand_name, "status": "rejection sent"})
            else:
                email_results.append({"resume_id": resume_id, "name": cand_name, "status": f"failed: {detail}"})

    return JSONResponse(content={"sent": len(email_results), "results": email_results})


@router.get("/status")
async def get_status():
    # get current session memory status

    return JSONResponse(content={
        "jd_uploaded": memory.job_description is not None,
        "resume_count": len(memory.resumes),
        "screening_done": len(memory.ranking) > 0
    })


@router.get("/report")
async def get_report():
    # return last generated report

    jd_text = memory.job_description
    if not jd_text:
        return JSONResponse(status_code=400, content={"error": "No JD uploaded"})

    if not memory.ranking:
        return JSONResponse(status_code=400, content={"error": "No screening done"})

    jd_analysis = analyze_jd(jd_text)
    job_type = jd_analysis.get("job_type", "experienced")

    # rebuild ranking list from memory for report
    ranking = []
    for resume_id in memory.ranking:
        score = memory.scores.get(resume_id, 0)
        # find resume info
        resume_info = None
        for r in memory.resumes:
            if r["id"] == resume_id:
                resume_info = r
                break
        parsed = {}
        if resume_info:
            parsed = parse_resume(resume_info["text"])
        ranking.append({"rank": len(ranking)+1, "score": score, "resume_id": resume_id, "parsed": parsed})

    report = generate_report(ranking, jd_text, job_type)
    return JSONResponse(content={"report": report})