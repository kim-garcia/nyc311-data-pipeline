"""First look at the NYC 311 Service Requests API."""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()  # Load variables from the .env file

API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
APP_TOKEN = os.getenv("NYC_APP_TOKEN")

params = {
    "$limit": 5,
    "$order": "created_date DESC",
}
headers = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

response = requests.get(API_URL, params=params, headers=headers, timeout=30)
response.raise_for_status()  # Stop with an error if the API call failed

records = response.json()
print(f"Records received: {len(records)}")
print(f"Columns in first record: {len(records[0])}")
print(json.dumps(records[0], indent=2))
