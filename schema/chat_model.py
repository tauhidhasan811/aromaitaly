from pydantic import BaseModel
# from typing import List, Dict
class ChatBody(BaseModel):
    user_query: str
    prev_info: str