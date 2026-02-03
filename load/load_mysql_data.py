import pandas as pd
from sqlalchemy import create_engine

DB_URL = "mysql+pymysql://root:root@localhost:3306/stock_db"
PARQUET_PATH = "/Users/apple/Documents/crypto-data-pipeline/data/processed/processed_data.parquet"

def load_to_mysql():
    engine = create_engine(DB_URL)
    df = pd.read_parquet(PARQUET_PATH)

    # Rename to match MySQL schema
    df = df.rename(columns={"name": "symbol"})

    df.to_sql(
        "stock_daily_prices",
        engine,
        if_exists="append",
        index=False
    )

    print("✅ Data loaded into MySQL")

if __name__ == "__main__":
    load_to_mysql()
