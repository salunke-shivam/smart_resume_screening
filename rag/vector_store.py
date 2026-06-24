import chromadb
from chromadb.config import Settings
import config
from rag.embeddings import create_embedding, create_embeddings

# setup chroma client
client = chromadb.PersistentClient(
    path=config.CHROMA_PERSIST_DIR,
    settings=Settings(anonymized_telemetry=False)
)


def get_jd_collection():
    # return job description collection
    
    return client.get_or_create_collection(config.COLLECTION_NAME_JD)


def get_resume_collection():
    # return resume collection
    
    return client.get_or_create_collection(config.COLLECTION_NAME_RESUME)


def add_job_description(jd_id, jd_text, metadata=None):
    # add a job description to vector db
    
    collection = get_jd_collection()
    vector = create_embedding(jd_text)
    
    if metadata is None:
        metadata = {}
    
    collection.add(
        ids=[jd_id],
        embeddings=[vector],
        documents=[jd_text],
        metadatas=[metadata]
    )


def add_resume(resume_id, resume_text, metadata=None):
    # add a resume to vector db
    
    collection = get_resume_collection()
    vector = create_embedding(resume_text)
    
    if metadata is None:
        metadata = {}
    
    collection.add(
        ids=[resume_id],
        embeddings=[vector],
        documents=[resume_text],
        metadatas=[metadata]
    )


def search_job_description(query_text, top_k=5):
    # search for similar job descriptions
    
    collection = get_jd_collection()
    query_vector = create_embedding(query_text)
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    return results


def search_resume(query_text, top_k=5):
    # search for similar resumes
    
    collection = get_resume_collection()
    query_vector = create_embedding(query_text)
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    return results


def clear_collections():
    # delete all data
    
    client.delete_collection(config.COLLECTION_NAME_JD)
    client.delete_collection(config.COLLECTION_NAME_RESUME)