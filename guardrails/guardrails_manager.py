from gateway.llm_gateway import call_llm


def is_resume(text):
    # check if text looks like a resume
    
    prompt = "Is this text a resume? Reply only yes or no.\n\n" + text[:2000]
    reply = call_llm(prompt)
    
    if reply and reply.strip().lower().startswith("yes"):
        return True
    return False


def is_job_description(text):
    # check if text looks like a job description
    
    prompt = "Is this text a job description? Reply only yes or no.\n\n" + text[:2000]
    reply = call_llm(prompt)
    
    if reply and reply.strip().lower().startswith("yes"):
        return True
    return False


def has_bias(text):
    # check for gender, age or ethnicity bias
    
    prompt = "Does this text contain bias about gender, age or ethnicity? Reply only yes or no.\n\n" + text[:2000]
    reply = call_llm(prompt)
    
    if reply and reply.strip().lower().startswith("yes"):
        return True
    return False


def clean_harmful_content(text):
    # remove harmful or toxic parts
    
    prompt = "Clean this text from harmful or inappropriate content. Return only cleaned text.\n\n" + text[:2000]
    reply = call_llm(prompt)
    
    if reply:
        return reply.strip()
    return text


def validate_input(text, doc_type="resume"):
    # check input before processing
    # doc_type: "resume" or "jd"
    
    if doc_type == "resume":
        if not is_resume(text):
            return False, "This does not look like a resume."
    else:
        if not is_job_description(text):
            return False, "This does not look like a job description."
    
    if has_bias(text):
        return False, "Text contains biased language."
    
    return True, "OK"


def validate_output(text):
    # check output before showing to user
    
    if has_bias(text):
        # try to clean bias
        return clean_harmful_content(text)
    
    return text