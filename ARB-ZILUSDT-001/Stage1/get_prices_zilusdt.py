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

# Function to fetch price from Zilswap
def get_zilswap_price(zusdt_token_address="zil1exampleaddress"):
    try:
        url = f"https://stats.zilswap.org/liquidity?pool=zil1sxx29cshups269ahh5qjffyr58mxjv9ft78jqy"
        response = requests.get(url, timeout=10)
        data = response.json()
        # Assuming the API returns pool reserves
        zil_amount = data.get('reserves', {}).get('ZIL', 0)
        zusdt_amount = data.get('reserves', {}).get('zUSDT', 0)
        if zil_amount and zusdt_amount:
            price = zusdt_amount / zil_amount  # Calculate ZIL/zUSDT price
            return {
                'bid': price,  # Simplified: using same price for bid/ask
                'ask': price,
                'timestamp': int(time.time() * 1000)
            }
        return None
    except Exception as e:
        print(f"Error fetching price from Zilswap: {e}")
        return None

# Function to compare prices
def compare_prices():
    kucoin_price = get_kucoin_price()
    zilswap_price = get_zilswap_price()

    if kucoin_price and zilswap_price:
        print("KuCoin prices:")
        print(f"Bid: {kucoin_price['bid']}, Ask: {kucoin_price['ask']}")
        print("Zilswap prices:")
        print(f"Bid: {zilswap_price['bid']}, Ask: {zilswap_price['ask']}")

        # Calculate arbitrage opportunities
        spread_buy = zilswap_price['bid'] - kucoin_price['ask']  # Buy on KuCoin, sell on Zilswap
        spread_sell = kucoin_price['bid'] - zilswap_price['ask']  # Buy on Zilswap, sell on KuCoin

        print(f"Arbitrage opportunity (Buy KuCoin, Sell Zilswap): {spread_buy:.6f} USDT")
        print(f"Arbitrage opportunity (Buy Zilswap, Sell KuCoin): {spread_sell:.6f} USDT")
    else:
        print("Failed to compare prices. Please try again.")

# Main execution
if __name__ == "__main__":
    while True:
        compare_prices()
        print("Waiting 10 seconds for the next update...")
        time.sleep(10)
