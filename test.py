# from components.core.clean_text import SelectedPreviousData
# data = {
#     "user_query": "are they avaiable from may 16 2026 to next 15 day",
#     "prev_info": "user_query: hi\nresponse: \"<p>Hello! How can I assist you with Joy Beach Villas or The View Villa today?</p>\"\nuser_query: how many villa are there\nresponse: \"<p>There are 13 villas at Joy Beach Villas:</p> <ul> <li>Beachfront Villa</li> <li>Deluxe Garden Villa</li> <li>Garden Villa 1</li> <li>Garden Villa 2</li> <li>Garden Villa 3</li> <li>Garden Villa 4</li> <li>Garden Villa 5</li> <li>Garden Pool Villa 1</li> <li>Garden Pool Villa 2</li> <li>Garden Pool Villa 3</li> <li>Garden Pool Villa 4</li> <li>Garden Pool Villa 5</li> <li>Garden Pool Villa 6</li> </ul>\"\nuser_query: give there price\nresponse: \"<ul> <li>Beachfront Villa: 11,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Beachfront Villa/334679\" target=\"_blank\">View Villa</a></li> <li>Deluxe Garden Villa: 14,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Deluxe Garden Villa/336039\" target=\"_blank\">View Villa</a></li> <li>Garden Villa 1: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Villa 1/336040\" target=\"_blank\">View Villa</a></li> <li>Garden Villa 2: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Villa 2/342568\" target=\"_blank\">View Villa</a></li> <li>Garden Villa 3: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Villa 3/342569\" target=\"_blank\">View Villa</a></li> <li>Garden Villa 4: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Villa 4/342570\" target=\"_blank\">View Villa</a></li> <li>Garden Villa 5: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Villa 5/342571\" target=\"_blank\">View Villa</a></li> <li>Garden Pool Villa 1: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Pool Villa 1/352148\" target=\"_blank\">View Villa</a></li> <li>Garden Pool Villa 2: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Pool Villa 2/352154\" target=\"_blank\">View Villa</a></li> <li>Garden Pool Villa 3: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Pool Villa 3/352156\" target=\"_blank\">View Villa</a></li> <li>Garden Pool Villa 4: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Pool Villa 4/352157\" target=\"_blank\">View Villa</a></li> <li>Garden Pool Villa 5: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Pool Villa 5/363730\" target=\"_blank\">View Villa</a></li> <li>Garden Pool Villa 6: 9,000 THB per night <a href=\"https://armaitoly-website.vercel.app/property/Garden Pool Villa 6/363731\" target=\"_blank\">View Villa</a></li> </ul> <span>No per person tax is applied. For more details, contact reception@joybeachvillas.com or WhatsApp +66 62 4080324.</span>\""
# }

# previous_info = data['prev_info']

# data = SelectedPreviousData(prev_info=previous_info)

# print(len(data))


# {
#     "user_query": "ok",
#     "prev_info": "user_query: hi\nresponse: \"<p>Hello! How can I assist you today?</p>\"\nuser_query: are the villas avaiable from 16 may 2026 to next 5 day\nresponse: \"All the villas are available from 16th May 2026 to 20th May 2026.\"\nuser_query: give the list\nresponse: \"Here is the list of available rooms from May 16 to May 20, 2026: 1. Beachfront Villa 2. Deluxe Garden Villa 3. Garden Villa 1 4. Garden Villa 2 5. Garden Villa 3 6. Garden Villa 4 7. Garden Villa 5 8. Garden Pool Villa 1 9. Garden Pool Villa 2 10. Garden Pool Villa 3 11. Garden Pool Villa 4 12. Garden Pool Villa 5 13. Garden Pool Villa 6\"\nuser_query: where are there price\nresponse: \"<p>The prices for the villas range from 9,000 to 14,000 THB per night. You can view the details of each villa by visiting the respective links.</p>\"\nuser_query: give villash with there price\nresponse: \"<p>The prices for the villas range from 9,000 to 14,000 THB per night. You can view the details of each villa by visiting the respective links.</p>\"\nuser_query: villah are there price\nresponse: \"<p>All the villas are available from 16th May 2026 to 20th May 2026.</p>\""
# }

import os
import json
from components.asset.get_all_villa import GetPriceAllVilla, GetAllVilla
from components.asset.validate_token import GetAccessToken

GetAccessToken()

print(os.environ["ACCESS_TOKEN_AI"])
data = GetPriceAllVilla()
# data = GetAllVilla()
print(data)
with open('data/all_villag_price.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)


