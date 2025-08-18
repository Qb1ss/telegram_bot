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

MIN_SPRADE_RANGE = 3
MAX_SPRADE_RANGE = 9
SPRADE_RANGE = random.randint(MIN_SPRADE_RANGE, MAX_SPRADE_RANGE)
COURSE_TOKEN = ton_price_usd * (100 - SPRADE_RANGE) / 100

char_limit = 6

def limit_to_chars(number):
    s = str(number)
    if len(s) <= char_limit:
        return s
    # Если число целое, обрезаем до 4 цифр
    if isinstance(number, int) or (isinstance(number, float) and number.is_integer()):
        return s[:char_limit]
    # Если число с плавающей точкой, стараемся сохранить точку
    if '.' in s:
        integer_part, fractional_part = s.split('.', 1)
        # Если целая часть >=4 символов, обрезаем её
        if len(integer_part) >= char_limit:
            return integer_part[:char_limit]
        # Иначе оставляем целую часть и добавляем дробную до 4 символов в сумме
        remaining_chars = char_limit - len(integer_part)
        return f"{integer_part}.{fractional_part[:remaining_chars - 1]}"
    return s[:char_limit]  # На всякий случай, если формат необычный

COURSE_TOKEN = limit_to_chars(COURSE_TOKEN)
COURSE_TOKEN = float(COURSE_TOKEN)