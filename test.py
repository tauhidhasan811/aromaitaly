import os
import json
import requests
from components.hyperparms import params

def flatten_feature_codes(feature_codes):
    flat_features = []

    for item in feature_codes:
        if isinstance(item, list):
            flat_features.extend(item)
        else:
            flat_features.append(item)

    return flat_features



header = {'token': 'WtDtBTbjXXe2HwsPURQ6xbJbNfn9DIW3/FCiQ902mz039qCZRfcnCpkD7dX67vOAE5i0CqhG+Zx0oVUvpLVuxBqnapzXWqqfXpb3hJyRfsq1/rTxikxk5mAQ1U1mM3bIuKMEA7DCPlzmPV32hyV96g=='}

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
        print(room_data)
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


# with open("data/v2_beds24_data.json", 'w', encoding='utf-8') as f:
#     json.dump(v2_json_data, f, indent=4)


# with open("data/v2_beds24_data.json", 'w', encoding='utf-8') as f:
#     json.dump(v2_json_data, f, indent=4)
