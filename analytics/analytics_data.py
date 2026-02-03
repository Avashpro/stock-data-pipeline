import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Optional: make plots look nicer
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

DB_URL = "mysql+pymysql://root:root@localhost:3306/stock_db"

def fetch_data():
    engine = create_engine(DB_URL)
    query = """
        SELECT *
        FROM stock_daily_prices
        WHERE symbol = 'AAPL'
        ORDER BY date
    """
    return pd.read_sql(query, engine)

def analytics(df):
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])

    # Moving averages
    df["ma_5"] = df["close_price"].rolling(5).mean()
    df["ma_20"] = df["close_price"].rolling(20).mean()

    # Latest close
    print("\n📊 Latest Close Price")
    print(df.tail(1)[["date", "close_price"]])

    # Price statistics
    print("\n📈 Price Statistics")
    print(df["close_price"].describe())

    # Highest volume day
    max_vol = df.loc[df["volume"].idxmax()]
    print("\n🔊 Highest Volume Day")
    print(max_vol[["date", "volume"]])

    # ------------------ PLOTS ------------------

    # 1️⃣ Close Price & Moving Averages
    plt.figure()
    plt.plot(df['date'], df['close_price'], label='Close Price', color='blue')
    plt.plot(df['date'], df['ma_5'], label='5-day MA', color='orange')
    plt.plot(df['date'], df['ma_20'], label='20-day MA', color='green')
    plt.title("AAPL Close Price and Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 2️⃣ Daily Volume
    plt.figure()
    sns.barplot(x='date', y='volume', data=df.tail(30), palette="viridis")  # last 30 days
    plt.title("AAPL Daily Trading Volume (Last 30 Days)")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 3️⃣ Price Histogram
    plt.figure()
    sns.histplot(df['close_price'], bins=30, kde=True, color='purple')
    plt.title("Distribution of AAPL Close Price")
    plt.xlabel("Close Price (USD)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = fetch_data()
    analytics(df)
