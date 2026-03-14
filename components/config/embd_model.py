from sentence_transformers import SentenceTransformer

def EmbeddedModel(model_name = "BAAI/bge-m3") -> SentenceTransformer:
    model = SentenceTransformer(model_name)
    return model