import os
import re
import json
from time import time
import shutil
from fastapi import FastAPI, Form, File, UploadFile
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
from components.core.clean_chunk_doc import format_retrieved_context, CleanVillaData
from components.hyperparms import params
from components.core.delete_path import force_delete_folder
from typing import Optional
from components.asset.avaiabality_tools import check_availability
from langchain.messages import HumanMessage, ToolMessage, SystemMessage
import tempfile
from components.core.wrapper import extract_document
from components.asset.validate_token import GetAccessToken
from components.core.clean_text import clean_previous_text
import datetime
from components.core.clean_text import SelectedPreviousData

load_dotenv()
# model = LoadGPT("gpt-4.1-nano-2025-04-14")
# model = LoadGPT("o4-mini-2025-04-16")
model = LoadGPT()


app = FastAPI()

app.state.expire_time = datetime.datetime.now()
# print(expire_time)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
embd_model = EmbeddedModel(model_name="BAAI/bge-small-en")
pool = embd_model.start_multi_process_pool()



def clean_text(text):
    return " ".join(text.split()).strip()

@app.post('/ai/api/update-knowledge')
async def update_knowledge(file: Optional[UploadFile]= File(None)):
    try:
        pool = embd_model.start_multi_process_pool()
        start_time = time()
        db_path = params['db_path']
        
        
        dir = 'data'
        if file is not None:
            ext = file.filename.split('.')[-1]
            accepted = ['pdf', 'docx']
            if ext not in accepted:
                return JSONResponse(
                    status_code=403,
                    content={
                        'status': False,
                        'status_code': 403,
                        'text': f"Invalid file format '{ext}' only accepted {accepted}"
                    }
                )
            file_name = f'notes.{ext}'

            file_path = os.path.join(dir, file_name)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(file_path)

        else:
            file_path= 'data/AI Website Bot notes JBV.docx'

        


        data = extract_document(file_path=file_path) 

        # path = 'AI Website Bot notes JBV.docx'
        # data = ReadDocx(path)
        chunks = CreatChunk(data=data)
        # room_info = str(GetRoomInformation())

        if datetime.datetime.now() >= app.state.expire_time:
            if GetAccessToken():
                app.state.expire_time = datetime.datetime.now() + datetime.timedelta(seconds=24 * 60 * 60)
            else:
                response = JSONResponse(
                    status_code=500,
                    content={
                        'status': False,
                        'status_code': 500,
                        'text': "Failed to create Access token. May Refresh token expire"
                    }
        )
        room_info = GetAllVilla()
        # print(room_info)
        # room_info = re.sub(r"[\[\]']", "", room_info)
        room_info = CleanVillaData(room_info)

        

        chunks.extend(room_info)

        # print(room_info)
        # with open('frewgtfzzall_villag.json', 'w', encoding='utf-8') as f:
        #     json.dump(chunks, f, indent=4)

        if os.path.isdir(db_path):
            # shutil.rmtree(db_path)
            force_delete_folder(db_path)
            print(f"Folder '{db_path}' and all its contents removed successfully.")
        else:
            print("No previous data")
            os.makedirs(db_path, exist_ok=True)
            
        # embds = embd_model.encode(chunks)
        embds = embd_model.encode_multi_process( chunks, pool )

        embd_model.stop_multi_process_pool(pool)

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
        end_time = time()
        minu = (end_time-start_time) // 60
        sec = (end_time-start_time) % 60
        print('*'* 80)
        print(' '*10, f"Total time take {minu} minutes and {sec} secound")
        print('*'* 80)

        
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
        user_query = data.user_query
        prev_unclean_info = data.prev_info
        prev_info = SelectedPreviousData(prev_unclean_info)
        print('=' * 80)
        print(f"Unclean data length : {len(prev_unclean_info)}")
        print(f"Clean data length : {len(prev_info)}")

        print('=' * 80)


        db_path = params['db_path']
        
        embd = embd_model.encode(data.user_query)

        collection = ChromaDB(db_path=db_path)

        if datetime.datetime.now() >= app.state.expire_time:
            if GetAccessToken():
                app.state.expire_time = datetime.datetime.now() + datetime.timedelta(seconds=24 * 60 * 60)

        results = collection.query(
            query_embeddings=[embd.tolist()],
            n_results=3
        )
        # print(results)

        context = format_retrieved_context(results)
        # print(context)
        prompt = RAGPrompt(user_query=user_query, 
                        previous_information=prev_info,
                        relevant_information=context)

        text = model.invoke(prompt)
        # print(text)
        if text.tool_calls:

            messages = [SystemMessage(content=
                                      """
                                        You are a specialized RAG AI assistant for Joy Beach Villas.
                                        Answer only using the provided Relevant Information and tool results.
                                        Use a formal and informative tone.

                                        Rules:

                                        1. Stay Duration:
                                        Minimun night stay: 
                                            {
                                                "Beachfront Villa": 3,
                                                "Deluxe Garden Villa": 3,
                                                "Garden Villa 1": 3,
                                                "Garden Villa 2": 3, 
                                                "Garden Villa 3": 3, 
                                                "Garden Villa 4": 3, 
                                                "Garden Villa 5": 3, 

                                                "Garden Pool Villa 1": 3,
                                                "Garden Pool Villa 2": 3,
                                                "Garden Pool Villa 3": 3,
                                                "Garden Pool Villa 4": 3,
                                                "Garden Pool Villa 5": 3,
                                                "Garden Pool Villa 6": 3
                                            }
                                        - If stay is LESS than Minimun night stay nights:
                                        → ONLY respond with:
                                            "The minimum stay requirement is Minimun night stay nights."
                                            then from from tools response suggest Minimun night stay nights to calclute Minimun night stay day from check-in date to next Minimun night stay day
                                            and Response Format and Booking Link format

                                        - If stay is Minimun night stay nights or MORE:
                                        → Show available villas normally

                                        2. Availability:
                                        - Only include villas available for the full requested stay.
                                        - Ignore unavailable villas.

                                        3. Response Format:
                                        - Use clean HTML (<p>, <ul>, <li>)

                                        4. Booking Link:
                                        <a href="https://armaitoly-website.vercel.app/property/{name}/{roomId}/checkAvailability?startDate={yyyymmdd}&endDate={yyyymmdd}" target="_blank">
                                        Book {name}
                                        </a>"""
            
                                    #   """
                                    #     You are a special RAG AI assistant for Joy Beach Villas.
                                    #     Answer will be based on the provided Relevant Information and tool results if a tool is used. 
                                    #     Tone will be formal and informative.

                                    #   Spacial note: 
                                    #   if user give more then 7 nights just follow the Response format note no need to say need stay minimun 7 day :
                                    #   elif user give less then 7 nights then just say You need minimun 7 day need to stay and same time give availablity of the 7 days from the check in date and also give the availability link.
                                      
                                    #   Response format note: 
                                    #   if any villa not avaiable for 7 nights then just ignore that villa and give the availability of the villa which is available for 7 nights and also give the availability link.
                                    #   if any villa avaible for 7 nights and still is after check in day still give the availablity.
                                    #   Response are give proper html tag like <p>, <li>, <ul>, or just serial number and If the answer mentions availability or check-in/check-out dates, and the property name and roomId are available, include the availability link:
                                    #   <a href="https://armaitoly-website.vercel.app/property/{name}/{roomId}/checkAvailability?startDate={yyyymmdd}&endDate={yyyymmdd}" target="_blank">Book {name}</a>"""

                            )]
            
            messages.extend([HumanMessage(content=data.user_query), text])

            for tool_call in text.tool_calls:
                # print(check_availability.description)
                tool_res = check_availability.invoke(tool_call["args"])
                print(tool_res)

                messages.append(
                    ToolMessage(
                        content=str(tool_res),
                        tool_call_id=tool_call["id"]
                    )
                )
            text = model.invoke(messages)

        text = clean_text(text.content)

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
