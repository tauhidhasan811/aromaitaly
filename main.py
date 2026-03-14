import os
import shutil
from fastapi import FastAPI
from dotenv import load_dotenv
from components.config.chromadb_config import ChromaDB
from components.core.file_reader import ReadDocx
from components.config.chunk_config import CreatChunk
from components.config.embd_model import EmbeddedModel
from components.core.store_chunk import StoreChunk
load_dotenv()
app = FastAPI()

@app.get('/ai/api/update-knowledge')
async def update_knowledge():

    path = 'chroma_db'
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"Folder '{path}' and all its contents removed successfully.")
    embd_model = EmbeddedModel()


    path = 'AI Website Bot notes JBV.docx'
    data = ReadDocx(path)


    chunks = CreatChunk(data=data)
    print('-' * 100)
    print(len(chunks))
    print('-' * 100)
    # print(chunks)

    embds = embd_model.encode(chunks)

    print(len(embds))
    print(f"Chunk length {len(chunks)} and Embedding length {len(embds)}")
    StoreChunk(data=chunks, embedding=embds, db_path=path)

    query = "Where are you"
    

    embd = embd_model.encode(query)

    collection = ChromaDB()

    results = collection.query(
        query_embeddings=[embd.tolist()],
        n_results=3
    )

    return results
