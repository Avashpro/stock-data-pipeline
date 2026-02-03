import requests
import pandas as pd
from datetime import datetime
import os

BASE_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=JFM8HCB5IGRSA111" 

def fetch_stock_data():
    all_data = []

    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

    data = response.json()

    if "Time Series (Daily)" not in data:
        print("API did not return daily data. Full response:")
        print(data)
        return pd.DataFrame()

    stock_data = data["Time Series (Daily)"]

    for key, value in stock_data.items():
        each_day = {
            "date": key,
            "open": value.get("1. open"),
            "high": value.get("2. high"),
            "low": value.get("3. low"),
            "close": value.get("4. close"),
            "volume": value.get("5. volume"),
            "name": data.get("Meta Data", {}).get("2. Symbol")
        }
        all_data.append(each_day)

    df = pd.DataFrame(all_data)

    df["date"] = pd.to_datetime(df["date"])
    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    return df

def save_raw_data(df):
    os.makedirs("data/raw", exist_ok=True)
    df["ingestion_time"] = datetime.utcnow()
    df.to_parquet("/Users/apple/Documents/crypto-data-pipeline/data/raw/feb3.parquet", index=False)
    print(f"✅ Saved {len(df)} records to Parquet")

if __name__ == "__main__":
    df = fetch_stock_data()
    if not df.empty:
        save_raw_data(df)
    else:
        print("No data fetched. Parquet not saved.")
