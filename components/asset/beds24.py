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


    def GetVillaInfo(self, property_name):

        fields = [
            "name", "propId", "currency", "address", "city", "state",
            "country", "postcode", "latitude", "longitude", "phone", "email", "web"
        ]

        FIELD_MAP = {
            "name": "name/proparty_name/villa_name",
            "latitude": "latitude/location",
            "latitude": "latitude/location",
            "country": "country/location",
            "city": "city/location",
            "state": "state/location",
            "postcode": "postcode/location",
        }

        url = "https://www.beds24.com/api/json/getProperty"

        payload = {
            "authentication": {
                "apiKey": self.apiKey,
                "propKey": os.environ.get(property_name)
            },
            "texts": ["EN"]
        }

        response = requests.post(url, json=payload)
        response = response.json()

        properties = response.get("getProperty", [])

        data = []

        for prop in properties:
            item = {}

            for field in fields:

                value = prop.get(field)

                # rename key using FIELD_MAP if exists
                new_field = FIELD_MAP.get(field, field)

                item[new_field] = value

            data.append(item)

        return data
    

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
        # location = data['getPropertyContent'][0]['texts'].get('propertyDescription1')
        # print(location)

        villa_info = self.GetVillaInfo(property_name)
        # print(villa_info)
        room_ids = [int(k) for k in room_data.keys() if k != "642098"]
        # print(room_ids)
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
        return villa_info, response['getPropertyContent'][0]['roomIds']