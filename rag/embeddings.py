from sentence_transformers import SentenceTransformer
import config

# load model once and reuse
model = None


def get_embedding_model():
    # return the same model every time
    
    global model
    
    if model is None:
        model = SentenceTransformer(config.EMBEDDING_MODEL)
    
    return model


def create_embedding(text):
    # convert text to vector
    
    model = get_embedding_model()
    vector = model.encode(text)
    return vector.tolist()


def create_embeddings(text_list):
    # convert list of texts to vectors
    
    model = get_embedding_model()
    vectors = model.encode(text_list)
    return vectors.tolist()