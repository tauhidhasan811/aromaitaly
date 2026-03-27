from langchain.tools import tool
from typing import List
from datetime import date
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def GetAccessToken():
    refreshToken = os.environ.get("REFRESH_TOKEN_AI")
    print(f"Refresh token is : {refreshToken}")

    headers = {
        "accept": "application/json",
        "refreshToken": refreshToken
    }

    url = "https://www.beds24.com/api/v2/authentication/token"
    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("Previous Token from env:", os.environ.get("ACCESS_TOKEN_AI"))
        os.environ["ACCESS_TOKEN_AI"] = data.get("token")

        print("Token:", data.get("token"))
        print("Current Token from env:", os.environ.get("ACCESS_TOKEN_AI"))
        print("Expires In:", data.get("expiresIn"))

        return True
    
    return False
    