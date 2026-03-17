
import json
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

