
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

import json

with open('room_data.json', 'r') as f:
    file = json.load(f)

for k, v in file.items():
    print(v)