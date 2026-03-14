import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()
@tool
def GetRoomContent():
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