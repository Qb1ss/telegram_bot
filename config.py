import random


#ТОКЕНЫ
TOKEN = "7891535798:AAGUtwq5OScPeG6pPP0j3IVx4EQDCA9SvC8"
#тестовый аккаунт (Тест тест)- 7502925852:AAGaTxKlJQNLjni_wxMW5fUt3FI4LQsGjMM
#тестовый аккаунт (Prospect Parsing News) - 7891535798:AAGUtwq5OScPeG6pPP0j3IVx4EQDCA9SvC8

#НАСТРОЙКИ
CURRENCY = "TRX"
TEST_MODE = True
COURSE = 3.182
MIN_EXCHANGE_VALUE = 20
MAX_EXCHANGE_VALUE = 1500
ACCOUNT_CHAR_COUNT = 3
PHOTO_ID = "https://static-cse.canva.com/blob/685034/vk1484.png"

#АДМИНЫ
ADMIN_ID = 1049864117
# блокировочный - 0000000000
# мой аккаунт - 1049864117

#ТЕКСТОВЫЕ СООБЩЕНИЯ
TEXT_START = "📊🔥<b>Your special bonus rate is active! (+7%)</b>\nYou have 5 bonus exchanges left.\n\nYour personal rate: <b>1 USDT ≈ 3.1413 TRX</b>💰\n\nPlease enter the amount of USDT (TRC-20) you want to exchange.\n\n<b>Limits:</b>\n- Minimum: <em>20 USDT</em>\n- Maximum: <em>1500 USDT</em>"
TEXT_ERROR_COUNT = f"Error: Enter the available amount (from {MIN_EXCHANGE_VALUE} to {MAX_EXCHANGE_VALUE})."
TEXT_EMAIL = "✅Great! Now, please enter your TRX wallet address (the one that starts with 'T')."
TEXT_ERROR_EMAIL = f"Error: Enter your Email address."
TEXT_ERROR_ACCOUNT = f"Error: your account is too short."

HEADER_ORDER_TEXT = f"<b>✅Your Exchange Order #{random.randint(30, 2300)} is Ready!✅</b>\n\n"
address_order_text = f"<code>01234567890</code>\n\n"
description_order_text = "<b>👇Deposit Address:👇</b>\n"
ADDRESS_ORDER_TEXT = description_order_text + address_order_text
WARNING_ORDER_TEXT = f"⚠️<b>IMPORTANT:</b>\n- send only USDT on the <b>{CURRENCY} (TRC-20)</b> network.\n- The order is valid for <b>30 minutes.</b>\n\nAfter sending the funds, press the button below."

#Информация
INFO_START = "(добавить генерацию процента (раз в день), бонус (будет отниматься) и курса)\n\n"

