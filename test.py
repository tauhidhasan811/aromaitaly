import os
import json
import requests




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
data = []
for prop in v2_json_data['data']:


    item = {}

    for field in fields:

        value = prop.get(field)

        # rename key using FIELD_MAP if exists
        new_field = FIELD_MAP.get(field, field)

        item[new_field] = value

    data.append(item)

with open("data/proparty_data.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)



# with open("data/v2_beds24_data.json", 'w', encoding='utf-8') as f:
#     json.dump(v2_json_data, f, indent=4)
