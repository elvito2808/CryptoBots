import ccxt
import requests
import time

# Function to fetch price from KuCoin
def get_kucoin_price():
    try:
        kucoin = ccxt.kucoin()
        ticker = kucoin.fetch_ticker('ZIL/USDT')
        return {
            'bid': ticker['bid'],
            'ask': ticker['ask'],
            'timestamp': ticker['timestamp']
        }
    except Exception as e:
        print(f"Error fetching price from KuCoin: {e}")
        return None

# Function to fetch price from Zilswap (commented out for now)
def get_zilswap_price():
    try:
        url = "https://api.zilswap.io/pairs/ZIL-zUSDT"  # Placeholder URL
        response = requests.get(url)
        data = response.json()
        return {
            'bid': data['bid'],
            'ask': data['ask'],
            'timestamp': data['timestamp']
        }
    except Exception as e:
        print(f"Error fetching price from Zilswap: {e}")
        return None

# Function to compare prices
def compare_prices():
    kucoin_price = get_kucoin_price()
    # zilswap_price = get_zilswap_price()  # Commented out to test KuCoin only

    if kucoin_price:
        print("KuCoin prices:")
        print(f"Bid: {kucoin_price['bid']}, Ask: {kucoin_price['ask']}")
    else:
        print("Failed to fetch KuCoin prices. Please try again.")

# Main execution
if __name__ == "__main__":
    while True:
        compare_prices()
        print("Waiting 10 seconds for the next update...")
        time.sleep(10)
