from rag.hybrid_search import compute_hybrid_score
import config


def _safe_ratio(value, total):
    # avoid division by zero
    if total == 0:
        return 0.0
    return min(value / total, 1.0)


def _extract_years(text):
    # try to get number of years from text like "5 years"
    if not text:
        return 0
    words = text.split()
    for i, word in enumerate(words):
        if "year" in word.lower():
            for j in range(i - 1, max(i - 3, -1), -1):
                try:
                    return int(words[j])
                except ValueError:
                    pass
    return 0




def score_candidate(resume_text, parsed_resume, jd_text, jd_analysis):
    job_type = jd_analysis.get("job_type", "experienced")

    # weights based on job type – now dominated by RAG similarity
    if job_type == "fresher":
        weights = {
            "rag_score": 0.70,       # semantic + keyword similarity
            "skills_match": 0.20,
            "education": 0.05,
            "projects": 0.05,
        }
    elif job_type == "internship":
        weights = {
            "rag_score": 0.65,
            "skills_match": 0.20,
            "education": 0.10,
            "projects": 0.05,
        }
    else:  # experienced
        weights = {
            "rag_score": 0.60,
            "skills_match": 0.25,
            "education": 0.05,
            "projects": 0.10,
        }

    # 1. hybrid RAG similarity (0-1)
    rag_score = compute_hybrid_score(resume_text, jd_text)

    # 2. direct skills match (0-1)
    required = jd_analysis.get("required_skills", [])
    good_have = jd_analysis.get("good_to_have_skills", [])
    all_required = required + good_have
    resume_skills = parsed_resume.get("skills", [])
    matched = 0
    for skill in resume_skills:
        skill_lower = skill.lower()
        for req in all_required:
            req_lower = req.lower()
            if skill_lower == req_lower or skill_lower in req_lower or req_lower in skill_lower:
                matched += 1
                break
    skills_score = _safe_ratio(matched, len(all_required)) if all_required else 1.0

    # 3. education (0 or 1)
    education = parsed_resume.get("education", "")
    edu_score = 1.0 if education else 0.0

    # 4. projects relevance (0-1)
    projects = parsed_resume.get("projects", [])
    if projects:
        proj_text = " ".join(projects)
        proj_score = compute_hybrid_score(proj_text, jd_text)
    else:
        proj_score = 0.0

    # combine
    overall = (weights["rag_score"] * rag_score +
               weights["skills_match"] * skills_score +
               weights["education"] * edu_score +
               weights["projects"] * proj_score)

    return round(overall * 100, 2)


def rank_candidates(candidates_list):
    # candidates_list is list of dicts with "resume_text", "parsed", "jd_text", "jd_analysis"
    # returns sorted list of dicts with rank and score

    scored = []
    for cand in candidates_list:
        score = score_candidate(
            cand["resume_text"],
            cand["parsed"],
            cand["jd_text"],
            cand["jd_analysis"]
        )
        scored.append({
            "resume_id": cand.get("resume_id", ""),
            "score": score,
            "parsed": cand["parsed"]
        })

    # sort descending by score
    scored.sort(key=lambda x: x["score"], reverse=True)
    for i, item in enumerate(scored):
        item["rank"] = i + 1

    return scored