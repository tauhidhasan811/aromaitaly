from components.config.chromadb_config import ChromaDB
from components.config.embd_model import EmbeddedModel

query = "Where are you"
model = EmbeddedModel()

embd = model.encode(query)

collection = ChromaDB()

results = collection.query(
    query_embeddings=[embd.tolist()],
    n_results=3
)

print(results)

# data = collection.get(include=["documents", "embeddings"])
# print(len(data["embeddings"]))