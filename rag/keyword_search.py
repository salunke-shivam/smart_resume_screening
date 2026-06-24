from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize

# download nltk tokenizer if not present
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# we keep separate indexes for jd and resume
jd_index = None
resume_index = None
jd_texts = []           # store original texts for lookup
resume_texts = []


def tokenize(text):
    # split text into words
    return word_tokenize(text.lower())


def build_jd_index(jd_list):
    # build bm25 index for job descriptions
    global jd_index, jd_texts
    jd_texts = jd_list
    tokenized = [tokenize(doc) for doc in jd_list]
    jd_index = BM25Okapi(tokenized)


def build_resume_index(resume_list):
    # build bm25 index for resumes
    global resume_index, resume_texts
    resume_texts = resume_list
    tokenized = [tokenize(doc) for doc in resume_list]
    resume_index = BM25Okapi(tokenized)


def search_jd_keywords(query, top_k=5):
    # search job descriptions by keywords
    if jd_index is None:
        return []
    tokens = tokenize(query)
    scores = jd_index.get_scores(tokens)
    # get top k results
    sorted_indices = sorted(range(len(scores)),
                            key=lambda i: scores[i],
                            reverse=True)[:top_k]
    results = []
    for idx in sorted_indices:
        results.append({
            "text": jd_texts[idx],
            "score": scores[idx]
        })
    return results


def search_resume_keywords(query, top_k=5):
    # search resumes by keywords
    if resume_index is None:
        return []
    tokens = tokenize(query)
    scores = resume_index.get_scores(tokens)
    # get top k results
    sorted_indices = sorted(range(len(scores)),
                            key=lambda i: scores[i],
                            reverse=True)[:top_k]
    results = []
    for idx in sorted_indices:
        results.append({
            "text": resume_texts[idx],
            "score": scores[idx]
        })
    return results


def clear_all():
    # reset everything
    global jd_index, resume_index, jd_texts, resume_texts
    jd_index = None
    resume_index = None
    jd_texts = []
    resume_texts = []