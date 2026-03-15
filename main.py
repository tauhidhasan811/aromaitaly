import os
import re
import shutil
from fastapi import FastAPI, Form
from dotenv import load_dotenv
from components.config.chromadb_config import ChromaDB
from components.core.file_reader import ReadDocx
from components.core.chunk_config import CreatChunk
from components.config.embd_model import EmbeddedModel
from components.core.store_chunk import StoreChunk
# from components.config.agent import CreateAgent
from components.asset.beds24 import GetRoomInformation
from components.config.openai_model import LoadGPT
from components.core.rag_prompt import RAGPrompt


load_dotenv()
model = LoadGPT()
app = FastAPI()
embd_model = EmbeddedModel()


def format_retrieved_context(results):
    documents = results.get("documents", [[]])
    metadatas = results.get("metadatas", [[]])

    docs = documents[0] if documents else []
    metas = metadatas[0] if metadatas else []

    if not docs:
        return "No relevant information found."

    formatted_chunks = []

    for i, doc in enumerate(docs):
        meta = metas[i] if i < len(metas) else {}
        meta = meta or {}   # important fix

        source = meta.get("source", "unknown")
        formatted_chunks.append(
            f"Source: {source}\nContent: {doc}"
        )

    return "\n\n---\n\n".join(formatted_chunks)


@app.get('/ai/api/update-knowledge')
async def update_knowledge():

    db_path = 'db/chroma_db'
    # embd_model = EmbeddedModel()


    if os.path.isdir(db_path):
        shutil.rmtree(db_path)
        print(f"Folder '{db_path}' and all its contents removed successfully.")
    else:
        print("No previous data")
        os.makedirs(db_path, exist_ok=True)

    path = 'AI Website Bot notes JBV.docx'
    data = ReadDocx(path)

    room_info = str(GetRoomInformation())
    room_info = re.sub(r"[\[\]']", "", room_info)

    chunks = CreatChunk(data=data)
  
    # print(chunks)
    chunks.append(str(room_info))
    print(room_info)
    print('-' * 60)

    print(len(chunks))
    print('-' * 60)
    print("Start embedding")
    embds = embd_model.encode(chunks)

    # print(embds[0])
    print(f"Chunk length {len(chunks)} and Embedding length {len(embds)}")
    StoreChunk(data=chunks, embedding=embds, db_path=db_path)

    

    # print(results)
    return "Store Successfully"


@app.post('/ai/api/check')
async def Check(user_query: str = Form(),
                prev_info: str = Form()):

    db_path = 'db/chroma_db'
    
    embd = embd_model.encode(user_query)

    collection = ChromaDB(db_path=db_path)


    results = collection.query(
        query_embeddings=[embd.tolist()],
        n_results=1
    )

    context = format_retrieved_context(results)

    prompt = RAGPrompt(user_query=user_query, 
                       previous_information=prev_info,
                       relevant_information=context)

    response = model.invoke(prompt).content

    return response