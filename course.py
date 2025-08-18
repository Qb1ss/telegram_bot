import requests
import random


def get_toncoin_price(vs_currency="usd"):
    coin_id = "the-open-network"  # ID Toncoin в CoinGecko
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[coin_id][vs_currency]
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


ton_price_usd = get_toncoin_price("usd")

if ton_price_usd is not None:
    print(f"Price of TON in USD: ${ton_price_usd}")
else:
    print("Couldn't get TON/USD exchange rate")

MIN_SPRADE_RANGE = 3
MAX_SPRADE_RANGE = 9
SPRADE_RANGE = random.randint(MIN_SPRADE_RANGE, MAX_SPRADE_RANGE)
COURSE_TOKEN = ton_price_usd * (100 - SPRADE_RANGE) / 100
