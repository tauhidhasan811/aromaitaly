
import os
import re
import shutil
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
from schema.chat_model import ChatBody

load_dotenv()
model = LoadGPT()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

def clean_text(text):
    return " ".join(text.split()).strip()

@app.get('/ai/api/update-knowledge')
async def update_knowledge():
    try:

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

        chunks.append(str(room_info))
        print(room_info)
        embds = embd_model.encode(chunks)

        # print(embds[0])
        print(f"Chunk length {len(chunks)} and Embedding length {len(embds)}")
        StoreChunk(data=chunks, embedding=embds, db_path=db_path)

        response = JSONResponse(
            status_code=200,
            content={
                'status': True,
                'status_code': 200,
                'text': "Store Successfully"
            }
        )
        return response

    except Exception as ex:
        response = JSONResponse(
            status_code=500,
            content={
                'status': False,
                'status_code': 500,
                'text': str(ex)
            }
        )
        return response


@app.post('/ai/api/chat-bot')
# async def Check(user_query: str = Form(),
#                 prev_info: str = Form()):
    
async def Check(data : ChatBody):
    

    try:
        db_path = 'db/chroma_db'
        
        embd = embd_model.encode(data.user_query)

        collection = ChromaDB(db_path=db_path)


        results = collection.query(
            query_embeddings=[embd.tolist()],
            n_results=1
        )

        context = format_retrieved_context(results)

        prompt = RAGPrompt(user_query=data.user_query, 
                        previous_information=data.prev_info,
                        relevant_information=context)

        text = model.invoke(prompt).content
        text = clean_text(text)

        response = JSONResponse(
            status_code=200,
            content={
                'status': True,
                'status_code': 200,
                'text': text
            }
        )
        return response

    except Exception as ex:
        response = JSONResponse(
            status_code=500,
            content={
                'status': False,
                'status_code': 500,
                'text': str(ex)
            }
        )
        return response
