import pandas as pd
import os

RAW_PATH = "/Users/apple/Documents/crypto-data-pipeline/data/raw/feb3.parquet"
PROCESSED_PATH = "/Users/apple/Documents/crypto-data-pipeline/data/processed/processed_data.parquet"

def transform_data():
    df = pd.read_parquet(RAW_PATH)

    # Rename columns for warehouse standard
    df = df.rename(columns={
        "open": "open_price",
        "high": "high_price",
        "low": "low_price",
        "close": "close_price"
    })

    # Ensure correct dtypes
    df["date"] = pd.to_datetime(df["date"])
    df["volume"] = df["volume"].astype("int64")

    # Sort time series
    df = df.sort_values("date")

    return df

def save_processed_data(df):
    os.makedirs("data/processed", exist_ok=True)
    df.to_parquet(PROCESSED_PATH, index=False)
    print(f"✅ Saved {len(df)} transformed records")

if __name__ == "__main__":
    df = transform_data()
    save_processed_data(df)
