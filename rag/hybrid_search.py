import numpy as np
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import nltk
from rag.embeddings import create_embedding
import config

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


def _cosine_similarity(vec1, vec2):
    # compute cosine between two vectors
    
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot / (norm1 * norm2)


def get_semantic_similarity(text1, text2):
    # semantic similarity using embeddings
    
    emb1 = create_embedding(text1)
    emb2 = create_embedding(text2)
    
    return _cosine_similarity(emb1, emb2)


def get_keyword_score(query_text, doc_text):
    # bm25 score for query against a single document
    
    tokens_doc = word_tokenize(doc_text.lower())
    tokens_query = word_tokenize(query_text.lower())
    
    if len(tokens_doc) == 0:
        return 0.0
    
    bm25 = BM25Okapi([tokens_doc])
    scores = bm25.get_scores(tokens_query)
    
    # scores is a list of one element
    return scores[0]


def compute_hybrid_score(resume_text, jd_text):
    # combine semantic and keyword scores
    
    sem_score = get_semantic_similarity(resume_text, jd_text)
    kw_score = get_keyword_score(resume_text, jd_text)
    
    # keyword score can be large, cap to 1.0 using tanh
    kw_score_norm = np.tanh(kw_score)
    
    final = (config.SEMANTIC_WEIGHT * sem_score) + \
            (config.KEYWORD_WEIGHT * kw_score_norm)
    
    return final