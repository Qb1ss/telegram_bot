from locale import currency

import telebot
import random


API_token = '7502925852:AAGaTxKlJQNLjni_wxMW5fUt3FI4LQsGjMM'
bot = telebot.TeleBot(API_token)
bonus = 5
tokens_user = ''

print("Bot is restarting")

@bot.message_handler(commands=['start'])
def welcome(message):
    present_line = random.randint(3, 7)
    currency_rate = random.randint(0, 3000)
    text = f"📊 🔥 <b>Your special bonus rate is active! (+{present_line}%)</b>\nYou have {bonus} bonus exchanges left.\n\nYour personal rate: <b>1 USDT ≈ 3.{currency_rate} TRX</b>💰\n\nPlease enter the amount of USDT (TRC-20) you want to exchange.\n\n<b>Limits:</b>\n- Minimum: <em>20 USDT</em>\n- Maximum: <em>1500 USDT</em>"
    bot.send_message(message.chat.id, text, parse_mode="HTML")

@bot.message_handler(func=lambda message: True)
def tokens(message):
    value = int(message.text)
    count_tokens = message.text

    if count_tokens.isdigit():
        if value < 20:
            bot.send_message(message.chat.id, "Минимальная транзакция 20 USDT", reply_markup=None, parse_mode="HTML")
        elif value > 1500:
            bot.send_message(message.chat.id, "Максимальная транзакция 1500 USDT", reply_markup=None, parse_mode="HTML")
        else:
            bot.send_message(callback.chat.id, "Введите вашу почту!", reply_markup=None, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Неверное значение. Попробуйте ещё раз", reply_markup=None)

@bot.callback_query_handler(func=lambda call: call.data)
def check_callback_data(callback):
    if callback == 'callback_mail':
        bot.send_message(callback.chat.id, "Введите вашу почту!", reply_markup=None, parse_mode="HTML")



bot.infinity_polling()
