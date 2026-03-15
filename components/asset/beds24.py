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
    Get property description from Beds24 relevant information about room, villa
    """
    data = GetRoomContent()
    room_data = data['getPropertyContent'][0]['roomIds']

    room_ids = [int(k) for k in room_data.keys()]

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
    # return the relevant room data
    return response['getPropertyContent'][0]['roomIds']