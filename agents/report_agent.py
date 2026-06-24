def generate_report(ranking, jd_text, job_type, top_n=5):
    # ranking is list from scoring_agent.rank_candidates
    # jd_text is the job description
    # job_type is "fresher"/"experienced"/"internship"
    # returns a formatted text report

    lines = []
    lines.append("=" * 50)
    lines.append("SMART RESUME SCREENER - REPORT")
    lines.append("=" * 50)
    lines.append("")
    lines.append(f"Job Type: {job_type.upper()}")
    lines.append("")
    lines.append("Job Description Summary:")
    # take first 300 chars of jd
    if len(jd_text) > 300:
        jd_summary = jd_text[:300] + "..."
    else:
        jd_summary = jd_text
    lines.append(jd_summary)
    lines.append("")
    lines.append("-" * 50)
    lines.append(f"TOP {top_n} CANDIDATES")
    lines.append("-" * 50)

    for cand in ranking[:top_n]:
        rank = cand["rank"]
        score = cand["score"]
        parsed = cand.get("parsed", {})
        name = parsed.get("name", "Unknown")
        email = parsed.get("email", "No email")
        skills = ", ".join(parsed.get("skills", []))
        lines.append(f"")
        lines.append(f"Rank #{rank} - Score: {score}/100")
        lines.append(f"Name: {name}")
        lines.append(f"Email: {email}")
        lines.append(f"Skills: {skills if skills else 'None listed'}")

    lines.append("")
    lines.append("=" * 50)
    lines.append("END OF REPORT")
    lines.append("=" * 50)

    return "\n".join(lines)