import os
import requests
import math
import pytz
from datetime import datetime


BASE_URL = "https://api.tfl.gov.uk"
LOCAL_TZ = pytz.timezone("Europe/London")


def _get_minutes_delta_from_date(iso_datetime):
    if iso_datetime is None:
        return ""

    now = datetime.now(tz=LOCAL_TZ)
    arrival_datetime = datetime.fromisoformat(iso_datetime.replace("Z", "+00:00"))

    time_difference_minutes = math.floor((arrival_datetime - now).total_seconds() / 60)

    return "due" if time_difference_minutes < 1 else f"{time_difference_minutes}m"


def get_bus_info():
    buses_data = []

    bus_stop_atco_code = "490012985W"

    response = requests.get(f"{BASE_URL}/StopPoint/{bus_stop_atco_code}/Arrivals", params={
        "app_key": os.environ.get("TFL_APP_KEY"),
    })

    if not response.status_code == 200:
        print(f"bad response from the TFL API: {response.status_code}")
        return buses_data

    response_body = response.json()

    items = sorted(response_body, key=lambda x: x.get("expectedArrival", ""))[:4]

    for item in items:
        buses_data.append({
            "line": item.get("lineName", ""),
            "due_time": _get_minutes_delta_from_date(item.get("expectedArrival")),
        })

    return buses_data
