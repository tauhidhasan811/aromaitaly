from langchain.tools import tool
from typing import List
from datetime import date
import requests
import os


@tool
def check_availability(room_ids: List[int], start_date: date, end_date: date):
    """Check room availability by room IDs and date interval. 
    room_ids come from previous information, and dates come from the user in YYYY-MM-DD format.
    and if user do not mension year the again tell them to give year and month and date
    """
    # header = {'token': 'WtDtBTbjXXe2HwsPURQ6xbJbNfn9DIW3/FCiQ902mz039qCZRfcnCpkD7dX67vOAE5i0CqhG+Zx0oVUvpLVuxBqnapzXWqqfXpb3hJyRfsq1/rTxikxk5mAQ1U1mM3bIuKMEA7DCPlzmPV32hyV96g=='}
    token = os.environ.get('ACCESS_TOKEN')
    header = {'token': token}

    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")

    room_query = "&".join([f"roomId={rid}" for rid in room_ids])

    url = f"https://www.beds24.com/api/v2/inventory/rooms/availability?{room_query}&startDate={start}&endDate={end}"

    response = requests.get(url, headers=header)

    if response.status_code != 200:
        return {
            "error": "API request failed",
            "status_code": response.status_code,
            "message": response.text
        }

    return response.json()