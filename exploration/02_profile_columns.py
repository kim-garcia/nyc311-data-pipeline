"""Profile a sample of NYC 311 records: which columns exist and how often they are empty"""

import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
APP_TOKEN = os.getenv("NYC_APP_TOKEN")
HEADERS = {"X-App-Token": APP_TOKEN} if APP_TOKEN else {}

PAGE_SIZE = 250
TOTAL_RECORDS = 1000


def fetch_page(offset: int) -> list[dict]:
    """Fetch one page of records starting at the given offset."""
    params = {
        "$limit": PAGE_SIZE,
        "$offset": offset,
        "$order": "created_date DESC, unique_key",
    }
    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


all_records = []
for offset in range(0, TOTAL_RECORDS, PAGE_SIZE):
    page = fetch_page(offset)
    print(f"Fetched {len(page)} records (offset {offset})")
    all_records.extend(page)
    if len(page) < PAGE_SIZE:
        break  # No more data available

df = pd.DataFrame(all_records)
print(f"\nTotal records: {len(df)}")
print(f"Total distinct columns: {len(df.columns)}")

null_pct = (df.isna().mean() * 100).round(1).sort_values(ascending=False)
print("\n% of records where each column is missing:")
print(null_pct.to_string())
