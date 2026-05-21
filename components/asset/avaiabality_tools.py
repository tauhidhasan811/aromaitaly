from langchain.tools import tool
from typing import List
from datetime import date
import datetime
import requests
import json
import os

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
end = tomorrow + datetime.timedelta(days=30)

description = f"""
        Check room availability by room IDs and date interval.
        And Year is {today.year}
        room_ids come from previous information, dates come from user in YYYY-MM-DD format.
        Current date is {today}.
        If user does not provide date, check availability from {tomorrow} to {end} and ask their preferred dates.
        if user give check-in and check-out date then just take the check in date and check-out date will be chech-out + 10 dayscheck availability
    """

@tool(description=description)
def check_availability(room_ids: List[int], start_date: date, end_date: date):
    # """
    #     Check room availability by room IDs and date interval.
    #     room_ids come from previous information, dates come from user in YYYY-MM-DD format.
    #     If user does not provide date, check availability from tomorrow ({datetime.datetime.now()}) for next 3 days and ask their preferred dates.
    # """
    description
    # header = {'token': 'WtDtBTbjXXe2HwsPURQ6xbJbNfn9DIW3/FCiQ902mz039qCZRfcnCpkD7dX67vOAE5i0CqhG+Zx0oVUvpLVuxBqnapzXWqqfXpb3hJyRfsq1/rTxikxk5mAQ1U1mM3bIuKMEA7DCPlzmPV32hyV96g=='}
    token = os.environ.get('ACCESS_TOKEN_AI')
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
    data = response.json()
    # with open('data/avaiablity.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, indent=4)
    return response.json()