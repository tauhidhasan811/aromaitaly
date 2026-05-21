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
from components.asset.get_all_villa import GetAllVilla, GetMinimumStayAllVilla
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

        # min_stay_info = GetMinimumStayAllVilla()
        # print(min_stay_info)
        # with open('data/min_stay_info.json', 'w', encoding='utf-8') as f:
        #     json.dump(min_stay_info, f, indent=4)

        

        with open('data/all_villa_without_clean.json', 'w', encoding='utf-8') as f:
            json.dump(room_info, f, indent=4)


        # print(room_info)
        # room_info = re.sub(r"[\[\]']", "", room_info)
        room_info = CleanVillaData(room_info)


        with open('data/all_villa_clean.json', 'w', encoding='utf-8') as f:
            json.dump(room_info, f, indent=4)

        # return

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

        min_stay_info = GetMinimumStayAllVilla()
        print(min_stay_info)
        # with open('data/min_stay_info.json', 'w', encoding='utf-8') as f:
        #     json.dump(min_stay_info, f, indent=4)
        # print(text)
        if text.tool_calls:

            messages = [SystemMessage(
                        content=f"""
                        You are a booking assistant for Joy Beach Villas.

                        Your job:
                        - Help users find available villas.
                        - Keep conversation natural.
                        - Never repeatedly ask for the same information.

                        BOOKING STATE RULES:

                        Required fields:
                        1. check-in date
                        2. check-out date
                        

                        Optional fields:
                        - adults: 0
                        - children: 0

                        IMPORTANT:
                        - If total guests are known but adults/children are missing:
                        assume:
                        numAdult = total guests
                        numChild = 0

                        - NEVER ask again for adults/children if total guests already exists.
                        - NEVER ask for information already provided in previous conversation.
                        - ALWAYS use previous conversation context.

                        AVAILABILITY RULES:
                        - Only show villas available for the full stay.
                        - Ignore unavailable villas.

                        MINIMUM STAY RULE:
                        {min_stay_info}

                        BEHAVIOR:
                        - Keep responses short and natural.
                        - Sound like a real booking assistant.
                        - Do not repeat unnecessary questions.
                        - If enough information exists, proceed directly.
                        - If user says "all villa", show all matching villas.
                        - If user changes dates, update booking context automatically.

                        BOOKING LINK:
                        <a href="https://aromaitaly.monirhrabby.com/property/{{name}}/{{roomId}}?startDate={{yyyymmdd}}&endDate={{yyyymmdd}}&numAdult={{numAdult}}&numChild={{numChild}}&nights={{number_of_nights}}&currency=THB" target="_blank">Book {{name}}</a>

                        OUTPUT:
                        - HTML only
                        - Allowed tags:
                        <p>, <ul>, <ol>, <li>, <a>, <br>

                        DO NOT:
                        - hallucinate
                        - ask repeated questions
                        - force adult/child split
                        - restart the booking flow
                        """
                        )]
                              
            messages.append({"Previous conversation": prev_info})
            # print(messages[0].content)
            
            messages.extend([HumanMessage(content=data.user_query), text])

            for tool_call in text.tool_calls:
                # print(check_availability.description)
                tool_res = check_availability.invoke(tool_call["args"])
                # print(tool_res)

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
