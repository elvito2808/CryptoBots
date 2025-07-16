import ccxt
import time
import requests
import json

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

# Function to fetch price from Zilswap using direct API
def get_zilswap_price():
    url = "https://api.zilliqa.com"
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "GetSmartContractState",
        "params": ["0x9c6e5a3d837b2c6a49e0c6b56e0cbaf76c35a8c6"]  # Zilswap router
    }
    try:
        response = requests.post(url, json=payload)
        state = response.json().get("result", {})
        pools = state.get("pools", {})
        zusdt_address = "0x818ca2e217e060ad17b7bd0124a483a1f66930a9"  # zUSDT
        zusdt_pool = pools.get(zusdt_address, {})
        zil_reserve = float(zusdt_pool.get("arguments", [0, 0])[0]) / 1e12  # ZIL (12 decimals)
        zusdt_reserve = float(zusdt_pool.get("arguments", [0, 0])[1]) / 1e6  # zUSDT (6 decimals)
        if zil_reserve and zusdt_reserve:
            fee_denom = 10000
            after_fee = 9970  # 0.3% fee
            price = (zusdt_reserve * after_fee) / (zil_reserve * fee_denom)  # Base price
            # Price Impact for 10,000 ZIL swap
            input_zil = 10000
            output_zusdt = (input_zil * zusdt_reserve * after_fee) / (zil_reserve * fee_denom + input_zil * after_fee)
            price_with_impact = output_zusdt / input_zil
            return {
                'bid': price,
                'ask': price,
                'price_with_impact_10000': price_with_impact,
                'timestamp': int(time.time() * 1000)
            }
        return None
    except Exception as e:
        print(f"Error fetching Zilswap state: {e}")
        return None

# Function to compare prices
def compare_prices():
    kucoin_price = get_kucoin_price()
    zilswap_price = get_zilswap_price()

    if kucoin_price and zilswap_price:
        print("KuCoin prices:")
        print(f"Bid: {kucoin_price['bid']:.8f}, Ask: {kucoin_price['ask']:.8f}")
        print("Zilswap prices:")
        print(f"Bid (small swap): {zilswap_price['bid']:.8f}")
        print(f"Bid (10,000 ZIL swap): {zilswap_price['price_with_impact_10000']:.8f}")
        print(f"Ask: {zilswap_price['ask']:.8f}")

        # Calculate arbitrage opportunities
        spread_buy = zilswap_price['bid'] - kucoin_price['ask']  # Buy on KuCoin, sell on Zilswap
        spread_sell = kucoin_price['bid'] - zilswap_price['ask']  # Buy on Zilswap, sell on KuCoin

        print(f"Arbitrage opportunity (Buy KuCoin, Sell Zilswap): {spread_buy:.8f} USDT")
        print(f"Arbitrage opportunity (Buy Zilswap, Sell KuCoin): {spread_sell:.8f} USDT")
    else:
        print("Failed to compare prices. Please try again.")

# Main execution
if __name__ == "__main__":
    while True:
        compare_prices()
        print("Waiting 10 seconds for the next update...")
        time.sleep(10)
