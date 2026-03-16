import os
import ast
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from components.hyperparms import params

load_dotenv()
class Beds24Data:
    def __init__(self):
        self.apiKey = os.environ.get("beds24_apiKey")
        
    def GetRoomContent(self, property_name):

        url = params['url']
        payload = {
            "authentication": {
                "apiKey": self.apiKey,
                "propKey": os.environ.get(property_name)
            },
            "texts": ["EN"]
        }
        response = requests.post(url, json=payload)

        return response.json()



    def GetRoomInformation(self, property_name):


        data = self.GetRoomContent(property_name)
        room_data = data['getPropertyContent'][0]['roomIds']
        room_ids = [int(k) for k in room_data.keys()]
        url = params['url']
        payload = {
            "authentication": {
                "apiKey": self.apiKey,
                "propKey": os.environ.get(property_name)
            },
            "roomIds": room_ids
        }

        response = requests.post(url, json=payload)
        response = response.json()
        return response['getPropertyContent'][0]['roomIds']