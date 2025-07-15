import ccxt
import requests
import time

# تابع برای گرفتن قیمت از KuCoin
def get_kucoin_price():
    try:
        # ایجاد نمونه از صرافی KuCoin با کتابخونه ccxt
        kucoin = ccxt.kucoin()
        # گرفتن داده‌های ticker برای جفت‌ارز ZIL/USDT
        ticker = kucoin.fetch_ticker('ZIL/USDT')
        # قیمت bid (بالاترین قیمت خرید) و ask (کمترین قیمت فروش)
        return {
            'bid': ticker['bid'],
            'ask': ticker['ask'],
            'timestamp': ticker['timestamp']
        }
    except Exception as e:
        print(f"خطا در گرفتن قیمت از KuCoin: {e}")
        return None

# تابع برای گرفتن قیمت از Zilswap
def get_zilswap_price():
    try:
        # فرض می‌کنیم Zilswap یه API ساده داره
        # این URL فقط نمونه‌ست، باید با API واقعی جایگزین بشه
        url = "https://api.zilswap.io/pairs/ZIL-zUSDT"
        response = requests.get(url)
        data = response.json()
        # فرض می‌کنیم API قیمت bid و ask رو برمی‌گردونه
        return {
            'bid': data['bid'],
            'ask': data['ask'],
            'timestamp': data['timestamp']
        }
    except Exception as e:
        print(f"خطا در گرفتن قیمت از Zilswap: {e}")
        return None

# تابع برای مقایسه قیمت‌ها
def compare_prices():
    kucoin_price = get_kucoin_price()
    zilswap_price = get_zilswap_price()

    if kucoin_price and zilswap_price:
        print("قیمت‌ها در KuCoin:")
        print(f"Bid: {kucoin_price['bid']}, Ask: {kucoin_price['ask']}")
        print("قیمت‌ها در Zilswap:")
        print(f"Bid: {zilswap_price['bid']}, Ask: {zilswap_price['ask']}")

        # محاسبه تفاوت قیمت (برای آربیتراژ)
        spread_buy = zilswap_price['bid'] - kucoin_price['ask']  # خرید از KuCoin، فروش در Zilswap
        spread_sell = kucoin_price['bid'] - zilswap_price['ask']  # خرید از Zilswap، فروش در KuCoin

        print(f"فرصت آربیتراژ (خرید از KuCoin، فروش در Zilswap): {spread_buy:.6f} USDT")
        print(f"فرصت آربیتراژ (خرید از Zilswap، فروش در KuCoin): {spread_sell:.6f} USDT")
    else:
        print("نمی‌تونم قیمت‌ها رو مقایسه کنم. لطفاً دوباره امتحان کن.")

# اجرای اسکریپت
if __name__ == "__main__":
    while True:
        compare_prices()
        print("منتظر 10 ثانیه برای به‌روزرسانی بعدی...")
        time.sleep(10)  # هر 10 ثانیه قیمت‌ها رو چک می‌کنه
