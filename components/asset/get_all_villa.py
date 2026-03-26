import os
import json
import requests
from dotenv import load_dotenv
from components.asset.beds24 import Beds24Data
from components.hyperparms import params

load_dotenv()





def flatten_feature_codes(feature_codes):
    flat_features = []

    for item in feature_codes:
        if isinstance(item, list):
            flat_features.extend(item)
        else:
            flat_features.append(item)

    return flat_features

"""
def GetAllVilla():
    beds24 = Beds24Data()
    properties = params["proparty_list"]
    fields = params["fields"]
    field_map = params["FIELD_MAP"]

    data = []

    # build grouped output keys using mapped field names
    field_lists = {
        field_map.get(field, field): []
        for field in fields
        if field != "name"
    }

    for proper in properties:
        print("-" * 60)
        print(" " * 25, proper)
        print("-" * 60)

        
        villa_info, file = beds24.GetRoomInformation(property_name=proper)
        missed_villaInfo = {
            "proparty": villa_info
        }
        # print(missed_villaInfo)
        for room_key, room_value in file.items():
            room = {"proparty": proper}

            for field in fields:
                # first get value using original source field name
                value = room_value.get(field)

                # special handling for featureCodes
                if field == "featureCodes" and value is not None:
                    value = flatten_feature_codes(value)

                # then rename only the output key
                new_field = field_map.get(field, field)
                room[new_field] = value

            data.append(room)

            for field in fields:
                if field == "name":
                    continue

                new_field = field_map.get(field, field)

                field_lists[new_field].append({
                    "proparty": proper,
                    "name": room.get(field_map.get("name", "name")),
                    "roomId": room.get(field_map.get("roomId", "roomId")),
                    new_field: room.get(new_field)
                })
    field_lists.update(missed_villaInfo)

    data = [
        {
            "field": field,
            "data": values
        }
        for field, values in field_lists.items()
    ]

    return data

# def GetAllVilla():
#     beds24 = Beds24Data()
#     properties = params["proparty_list"]
#     fields = params["fields"]

#     data = []

#     field_lists = {field: [] for field in fields if field != "name"}

#     for proper in properties:
#         print("-" * 60)
#         print(" " * 25, proper)
#         print("-" * 60)

#         file = beds24.GetRoomInformation(property_name=proper)

#         for room_key, room_value in file.items():
#             room = {"proparty": proper}

#             for field in fields:
#                 room[field] = room_value.get(field)

#             if "featureCodes" in room_value:
#                 features = []
#                 for fec in room_value["featureCodes"]:
#                     if isinstance(fec, list):
#                         features.extend(fec)
#                     else:
#                         features.append(fec)
#                 room["features"] = features

#             data.append(room)

#             for field in fields:
#                 if field == "name":
#                     continue

#                 field_lists[field].append({
#                     "proparty": proper,
#                     "name": room.get("name"),
#                     field: room.get(field)
#                 })

#     # convert dict → list
#     return [
#         {"field": field, "data": values}
#         for field, values in field_lists.items()
#     ]



# def GetAllVilla():
#     beds24 = Beds24Data()
#     data = []
#     properties = params['proparty_list']
#     for proper in properties:
#         print('-' * 60)
#         print(' ' * 25, proper)
#         print('-' * 60)

#         file = beds24.GetRoomInformation(property_name=proper)
#         for room_key, room_value in file.items():

#             room = {}
#             room['proparty'] = proper
#             for k1, v1 in room_value.items():
#                 if k1 == 'featureCodes':
#                     feature = []
#                     for fec in v1:
#                         feature.extend(fec)
#                     room['name'] = name
                    
#                 elif k1 == "name":
#                     name = v1
#                 else:
#                     room[k1] = v1
                    
            
#             room['features'] = feature

#             data.append(room)
#     print(f"Total get : {len(data)} villa")
#     return data
    


#     # with open('all_villag.json', 'w', encoding='utf-8') as f:
#     #     json.dump(data, f, indent=4)

"""

def GetAllVilla():
    # header = {'token': 'WtDtBTbjXXe2HwsPURQ6xbJbNfn9DIW3/FCiQ902mz039qCZRfcnCpkD7dX67vOAE5i0CqhG+Zx0oVUvpLVuxBqnapzXWqqfXpb3hJyRfsq1/rTxikxk5mAQ1U1mM3bIuKMEA7DCPlzmPV32hyV96g=='}
    token = os.environ.get('ACCESS_TOKEN')
    header = {'token': token}

    url = 'https://www.beds24.com/api/v2/properties?includeTexts=all&includeAllRooms=true'

    response = requests.get(url, headers=header)
    v2_json_data = response.json()

    villa_info = []
    fields = [
                "name", "id", "currency", "address", "city", "state",
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
    proparty_info = []
    for prop in v2_json_data['data']:


        item = {}

        for field in fields:

            value = prop.get(field)

            # rename key using FIELD_MAP if exists
            new_field = FIELD_MAP.get(field, field)

            item[new_field] = value

        proparty_info.append(item)

    with open("data/proparty_data.json", 'w', encoding='utf-8') as f:
        json.dump(proparty_info, f, indent=4)


    missed_villaInfo = {
                "proparty": proparty_info
            }

    # properties = params["proparty_list"]
    fields = params["fields"]
    field_map = params["FIELD_MAP"]

    data = []

    # build grouped output keys using mapped field names
    field_lists = {
        field_map.get(field, field): []
        for field in fields
        if field != "name"
    }



    for proper_data in v2_json_data['data']:
        print("-" * 60)
        print(" " * 25, proper_data['name'])
        print("-" * 60)

            
            # villa_info, file = beds24.GetRoomInformation(property_name=proper)
            
            # print(missed_villaInfo)
        for room_data in proper_data['roomTypes']:
            # print(room_data)
            # for room_key, room_value in room_data.items():
            #     print(room_key, room_value)
            room = {"proparty": proper_data['name']}
            

            for field in fields:
                # first get value using original source field name
                value = room_data.get(field)

                #  special handling for featureCodes
                if field == "featureCodes" and value is not None:
                    value = flatten_feature_codes(value)

                # then rename only the output key
                new_field = field_map.get(field, field)
                room[new_field] = value

            data.append(room)

            for field in fields:
                if field == "name" or field == 'id':
                    continue
                if room.get('id') == 337089 or room.get('id') == 642098:
                    continue

                new_field = field_map.get(field, field)

                field_lists[new_field].append({
                        "proparty": proper_data['name'],
                        "name": room.get(field_map.get("name", "name")),
                        "roomId": room.get(field_map.get("id", "id")),
                        new_field: room.get(new_field)
                    })
        field_lists.update(missed_villaInfo)

        data = [
            {
                "field": field,
                "data": values
            }
            for field, values in field_lists.items()
        ]

    with open("data/v2_beds24_room_data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    return data


    # with open("data/v2_beds24_data.json", 'w', encoding='utf-8') as f:
    #     json.dump(v2_json_data, f, indent=4)


    # with open("data/v2_beds24_data.json", 'w', encoding='utf-8') as f:
    #     json.dump(v2_json_data, f, indent=4)
