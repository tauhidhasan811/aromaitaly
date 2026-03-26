from langchain.tools import tool
from typing import List
from datetime import date
import requests
import os


def RefreshAccessToken():
    refreshToken = os.environ.get("REFRESH_TOKEN")

    if not refreshToken:
        raise ValueError("REFRESH_TOKEN not found in environment variables")

    headers = {
        "accept": "application/json",
        "refreshToken": refreshToken
    }

    url = "https://www.beds24.com/api/v2/authentication/token"
    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        os.environ["ACCESS_TOKEN"] = data.get("token")

        print("Token:", data.get("token"))
        print("Expires In:", data.get("expiresIn"))

        return data.get("token")
    else:
        print("Error:", response.text)
        return None