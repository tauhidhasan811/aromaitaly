
import json
from dotenv import load_dotenv
from components.asset.beds24 import Beds24Data
from components.hyperparms import params
load_dotenv()

def GetAllVilla():
    beds24 = Beds24Data()
    data = []
    properties = params['proparty_list']
    for proper in properties:
        print('-' * 60)
        print(' ' * 25, proper)
        print('-' * 60)

        file = beds24.GetRoomInformation(property_name=proper)
        for room_key, room_value in file.items():

            room = {}
            room['proparty'] = proper
            for k1, v1 in room_value.items():
                if k1 == 'featureCodes':
                    feature = []
                    for fec in v1:
                        feature.extend(fec)
                    room['name'] = name
                    
                elif k1 == "name":
                    name = v1
                else:
                    room[k1] = v1
                    
            
            room['features'] = feature

            data.append(room)
    print(f"Total get : {len(data)} villa")
    return data
    


    # with open('all_villag.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, indent=4)

