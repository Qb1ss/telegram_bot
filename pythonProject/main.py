import telebot


token = '7502925852:AAGaTxKlJQNLjni_wxMW5fUt3FI4LQsGjMM'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.first_name
    text = "📊 🔥 <b>Your special bonus rate is active! (+7%)</b>\nYou have 5 bonus exchanges left.\n\nYour personal rate: <b>1 USDT ≈ 3.1413 TRX</b>💰\n\nPlease enter the amount of USDT (TRC-20) you want to exchange.\n\n<b>Limits:</b>\n- Minimum: <em>20 USDT</em>\n- Maximum: <em>1500 </em>"
    bot.send_message(message.chat.id, text, parse_mode="HTML")


bot.infinity_polling()

