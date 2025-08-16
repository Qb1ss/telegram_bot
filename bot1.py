import re
import sqlite3
from telebot import TeleBot, types
from config import (
    TOKEN, ADMIN_ID,
    TEST_MODE, CURRENCY, COURSE, MIN_EXCHANGE_VALUE, MAX_EXCHANGE_VALUE,
    TEXT_START, INFO_START, TEXT_ERROR_COUNT, TEXT_EMAIL, TEXT_ERROR_EMAIL,
    TEXT_ERROR_ACCOUNT,ACCOUNT_CHAR_COUNT, PHOTO_ID,
    HEADER_ORDER_TEXT, ADDRESS_ORDER_TEXT, WARNING_ORDER_TEXT)
from datetime import datetime
import random


bot = TeleBot(TOKEN)
sum_user_count = 0
user_count = 0
user_account = ""

offer_order_text = f"Please send <b>exactly {user_count}. а USDT (TRC-20)</b> to the address below.\n\n"
user_account_text = f"You will receive: <b>{sum_user_count * COURSE} TRX</b>\nTo your wallet:\n<code>{user_account}</code>\n\n"

now = datetime.now()
print(f'The bot restarted at {now}')

# ==== БАЗА ДАННЫХ ====
def init_db():
    conn = sqlite3.connect("data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            digits INTEGER,
            email TEXT,
            comment TEXT
        )
    """)
    conn.commit()
    conn.close()


def set_field(field, user_id, value):
    conn = sqlite3.connect("data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    cursor.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, user_id))
    conn.commit()
    conn.close()


def get_user_data(user_id):
    conn = sqlite3.connect("data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT digits, email, comment FROM users WHERE user_id=?", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data


def get_all_users():
    conn = sqlite3.connect("data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, digits, email, comment
        FROM users
        WHERE digits IS NOT NULL
          AND email IS NOT NULL
          AND comment IS NOT NULL
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def clear_user_data(user_id):
    conn = sqlite3.connect("data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()


# ==== УТИЛИТЫ ===
def reset_user(message, text="Анкета сброшена"):
    clear_user_data(message.chat.id)
    try:
        bot.clear_step_handler_by_chat_id(message.chat.id)
    except Exception:
        pass
    if text and text.strip():
        bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())


# ==== АНКЕТА ====
def start_flow(message):
    #if message.chat.id == ADMIN_ID:
    #    bot.send_message(ADMIN_ID, "Администратор не заполняет анкету.")
    #    return

    reset_user(message, text="")

    if message.chat.id == ADMIN_ID:
        text_start = INFO_START + TEXT_START


    text_start = TEXT_START
    snt_msg = bot.send_message(message.chat.id, text_start, parse_mode="HTML")
    bot.register_next_step_handler(snt_msg, step_digits)


def step_digits(message):
    if not message.text or not message.text.isdigit():
        sent = bot.send_message(message.chat.id, TEXT_ERROR_COUNT)
        bot.register_next_step_handler(sent, step_digits)
        return
    value = int(message.text)
    user_count = value
    sum_user_count = value * COURSE

    if MIN_EXCHANGE_VALUE <= value <= MAX_EXCHANGE_VALUE:
        set_field("digits", message.chat.id, value)
        text_sum = f"✅Great! You are exchanging <b>{user_count} USDT.</b>\nYou will receive approximately: <b>{sum_user_count} {CURRENCY}.</b>\nPlease enter your emaiI address to continue."
        sent = bot.send_message(message.chat.id, text_sum, parse_mode="HTML")
        bot.register_next_step_handler(sent, step_email)
    else:
        sent = bot.send_message(message.chat.id, TEXT_ERROR_COUNT)
        bot.register_next_step_handler(sent, step_digits)


def step_email(message):
    if message.text and re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        set_field("email", message.chat.id, message.text)
        sent = bot.send_message(message.chat.id, TEXT_EMAIL)
        bot.register_next_step_handler(sent, step_comment)
    else:
        sent = bot.send_message(message.chat.id, TEXT_ERROR_EMAIL)
        bot.register_next_step_handler(sent, step_email)


def step_comment(message):
    if not message.text or len(message.text) < ACCOUNT_CHAR_COUNT:
        sent = bot.send_message(message.chat.id, TEXT_ERROR_ACCOUNT)
        bot.register_next_step_handler(sent, step_comment)
        return
    set_field("comment", message.chat.id, message.text)
    user_account = message.text

    order_text = HEADER_ORDER_TEXT + offer_order_text + ADDRESS_ORDER_TEXT + user_account_text + WARNING_ORDER_TEXT

    # Получаем данные пользователя
    data = get_user_data(message.chat.id)
    digits, email, comment = data

    # Отправляем админу
    bot.send_message(ADMIN_ID, f"📩 Новая заявка:\nЧисло: {digits}²\nEmail: {email}\nКомментарий: {comment}")

    # Отправляем фото от бота пользователю (здесь нужно указать file_id заранее)

    bot.send_photo(message.chat.id, PHOTO_ID)

    # Сообщение пользователю
    bot.send_message(message.chat.id, order_text, parse_mode="HTML",
                     reply_markup=types.ReplyKeyboardRemove())

    # Предлагаем заполнить снова
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Заполнить снова")
    sent = bot.send_message(message.chat.id, "Хотите заполнить анкету снова?", reply_markup=markup)
    bot.register_next_step_handler(sent, wait_restart)


def wait_restart(message):
    if message.text and message.text.strip().lower() == "заполнить снова":
        start_flow(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Заполнить снова")
        sent = bot.send_message(message.chat.id, "Нажмите кнопку «Заполнить снова» для перезапуска анкеты.",
                                reply_markup=markup)
        bot.register_next_step_handler(sent, wait_restart)


# ==== ПОКАЗ ЗАЯВОК АДМИНУ ====
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.text == "Показать заявки")
def show_all(message):
    data = get_all_users()
    if not data:
        bot.send_message(ADMIN_ID, "📭 Заявок пока нет.")
        return
    for user_id, digits, email, comment in data:
        bot.send_message(ADMIN_ID, f"👤 ID: {user_id}\n📏 {digits}²\n📧 {email}\n💬 {comment}")


# ==== КОМАНДЫ ====
@bot.message_handler(commands=["start", "restart"])
def start_cmd(message):
    if message.chat.id == ADMIN_ID:
        if TEST_MODE == False:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Показать заявки")
            bot.send_message(ADMIN_ID, "Добро пожаловать, админ!", reply_markup=markup)
    else:
        start_flow(message)


@bot.message_handler(func=lambda m: m.text and m.text.strip().lower() == "заполнить снова")
def restart(message):
    start_flow(message)


if __name__ == "__main__":
    init_db()
    bot.polling(none_stop=True)
