from components.config.chromadb_config import ChromaDB
import uuid

def StoreChunk(data, embedding, db_path):

    print(f"Chunk length {len(data)} and Embedding length {len(embedding)}")
    if len(data) != len(embedding):
        raise ValueError("Chunks and embeddings length mismatch")

    # client = chromadb.PersistentClient(path="chroma_db")

    # collection = client.get_or_create_collection("docx_info")
    collection = ChromaDB(db_path=db_path)
    for chunk, emb in zip(data, embedding):

        # print(emb.tolist())
        collection.add(
            documents=[chunk],
            embeddings=[emb],
            ids=[str(uuid.uuid4())]
        )

    print("Stored:", len(data))

# import chromadb
# import uuid

# def StoreChunk(data, embedding):

#     client = chromadb.PersistentClient(path="chroma_db")

#     collection = client.get_or_create_collection(
#         name="docx_info"
#     )

#     for idx, chunk in enumerate(data):

#         collection.add(
#             documents=[chunk],
#             embeddings=[embedding[idx].tolist()],
#             ids=[str(uuid.uuid4())]
#         )

#     print("Chunks stored successfully")