
# from components.config.embd_model import EmbeddedModel



# # data = collection.get(include=["documents", "embeddings"])
# # print(len(data["embeddings"]))


# from components.config.chromadb_config import ChromaDB
# from components.core.file_reader import ReadDocx
# from components.config.chunk_config import CreatChunk
# from components.config.embd_model import EmbeddedModel
# from components.core.store_chunk import StoreChunk

# path = 'AI Website Bot notes JBV.docx'

# data = ReadDocx(path)
# print('*' * 100)
# # print(data)
# print('*' * 100)

# chunks = CreatChunk(data=data)
# print('-' * 100)
# print(len(chunks))
# print('-' * 100)
# # print(chunks)

# embds = EmbeddedModel().encode(chunks)

# print(len(embds))
# print(f"Chunk length {len(chunks)} and Embedding length {len(embds)}")
# StoreChunk(data=chunks, embedding=embds)

# query = "Where are you"
# model = EmbeddedModel()

# embd = model.encode(query)

# collection = ChromaDB()

# results = collection.query(
#     query_embeddings=[embd.tolist()],
#     n_results=3
# )

# print(results)



# import os
# import shutil

# folder_path = "chroma_db"

# # Check if the folder exists before attempting to remove it
# if os.path.isdir(folder_path):
#     shutil.rmtree(folder_path)
#     print(f"Folder '{folder_path}' and all its contents removed successfully.")
# else:
#     print(f"Folder '{folder_path}' not found or is not a directory.")

# import requests

# url = "https://www.beds24.com/api/json/getPropertyContent"

# payload = {
#     "authentication": {
#         "apiKey": "h12j3123h123j28z",
#         "propKey": "Joybeach8754h6fdr5"
#     },
#     "texts": ["EN"]
# }

# headers = {
#     "Content-Type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.status_code)
# print(response.json())

import json
# from components.asset.beds24 import GetRoomContent, GetRoomInformation

# # data = GetRoomContent()

# # with open('data.json', 'w', encoding='utf-8') as f:
# #     json.dump(data,f, indent=4)
# with open('data.json', 'r' ,encoding='utf-8') as f:

#     data = json.load(f)


# room_data = data['getPropertyContent'][0]['roomIds']

# print(room_data)
# room_ids = []
# for k, v in room_data.items():
#     room_ids.append(int(k))

# print(room_ids)

# room_info = GetRoomInformation()

# print(str(room_info))


# print(room_info)
# with open('room_data.json', 'w', encoding='utf-8') as f:
#     json.dump(room_info['getPropertyContent'][0]['roomIds'], f, indent=4)


# from components.config.openai_model import LoadGPT
# from dotenv import load_dotenv

# load_dotenv()
# model = LoadGPT()

# print(model.invoke("Hi"))

# with open('response_1773554258824.json', 'r' ,encoding='utf-8') as f:

#     data = json.load(f)


# print(data['messages'][1]['content'])
# from components.asset.beds24 import Beds24Data

# beds24 = Beds24Data()

# data = beds24.GetRoomInformation(property_name="joy_beach_villa")
# print(data)


# import json
# from dotenv import load_dotenv
# from components.asset.beds24 import Beds24Data
# from components.hyperparms import params
# load_dotenv()

# beds24 = Beds24Data()
# data = []
# properties = params['proparty_list']
# for proper in properties:
#     print('-' * 60)
#     print(' ' * 25, proper)
#     print('-' * 60)

#     file = beds24.GetRoomInformation(property_name=proper)
#     for room_key, room_value in file.items():

#         room = {}
#         room['proparty'] = proper
#         for k1, v1 in room_value.items():
#             if k1 == 'featureCodes':
#                 feature = []
#                 for fec in v1:
#                     feature.extend(fec)
#                 room['name'] = name
                
#             elif k1 == "name":
#                 name = v1
#             else:
#                 room[k1] = v1
                
        
#         room['features'] = feature

#         data.append(room)
#     print(f"Total get : {len(data)} villa")

# with open('all_villag.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, indent=4)


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
# from components.asset.beds24 import GetRoomInformation
from components.config.openai_model import LoadGPT
from components.core.rag_prompt import RAGPrompt
from schema.chat_model import ChatBody
from components.asset.get_all_villa import GetAllVilla
from components.core.clean_chunk_doc import format_retrieved_context
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




def clean_text(text):
    return " ".join(text.split()).strip()

@app.get('/ai/api/update-knowledge')
async def update_knowledge():
    try:

        db_path = 'chroma_db'

        if os.path.isdir(db_path):
            shutil.rmtree(db_path)
            print(f"Folder '{db_path}' and all its contents removed successfully.")
        else:
            print("No previous data")
            os.makedirs(db_path, exist_ok=True)

        path = 'AI Website Bot notes JBV.docx'
        data = ReadDocx(path)

        # room_info = str(GetRoomInformation())
        room_info = GetAllVilla()
        # room_info = re.sub(r"[\[\]']", "", room_info)

        chunks = CreatChunk(data=data)

        chunks.append(room_info)
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