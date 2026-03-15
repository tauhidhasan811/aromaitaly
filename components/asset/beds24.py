import os
import ast
import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

def GetRoomContent():
    """
    Get property description from Beds24
    """
    url = "https://www.beds24.com/api/json/getPropertyContent"

    payload = {
        "authentication": {
            "apiKey": os.environ.get("beds24_apiKey"),
            "propKey": os.environ.get("propKey")
        },
        "texts": ["EN"]
    }

    response = requests.post(url, json=payload)

    return response.json()


# @tool
def GetRoomInformation():
    """
    Get property description from Beds24
    """

    data = GetRoomContent()

    room_data = data['getPropertyContent'][0]['roomIds']

    # print(room_data)
    room_ids = []
    for k, v in room_data.items():
        room_ids.append(int(k))

    # print(room_ids)

        
    url = "https://www.beds24.com/api/json/getPropertyContent"

    payload = {
        "authentication": {
            "apiKey": os.environ.get("beds24_apiKey"),
            "propKey": os.environ.get("propKey")
        },
        "roomIds": room_ids
    }

    response = requests.post(url, json=payload)
    response = response.json()
    print(response)
    response = response['getPropertyContent'][0]['roomIds']
    return response