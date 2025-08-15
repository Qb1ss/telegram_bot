import re
import sqlite3
from telebot import TeleBot, types
from config import TOKEN, ADMIN_ID


bot = TeleBot(TOKEN)


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


# ==== УТИЛИТЫ ====
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
    if message.chat.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, "Администратор не заполняет анкету.")
        return
    reset_user(message, text="")
    bot.send_message(message.chat.id, "Начнем заполнение анкеты", reply_markup=types.ReplyKeyboardRemove())
    snt_msg = bot.send_message(message.chat.id, "Введите число в квадрате (от 20 до 150):")
    bot.register_next_step_handler(snt_msg, step_digits)


def step_digits(message):
    if not message.text or not message.text.isdigit():
        sent = bot.send_message(message.chat.id, "Ошибка: Введите число в квадрате (от 20 до 150).")
        bot.register_next_step_handler(sent, step_digits)
        return
    value = int(message.text)
    if 20 <= value <= 150:
        set_field("digits", message.chat.id, value)
        sent = bot.send_message(message.chat.id, "Введите ваш email:")
        bot.register_next_step_handler(sent, step_email)
    else:
        sent = bot.send_message(message.chat.id, "Ошибка: введите число в квадрате (от 20 до 150).")
        bot.register_next_step_handler(sent, step_digits)


def step_email(message):
    if message.text and re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        set_field("email", message.chat.id, message.text)
        sent = bot.send_message(message.chat.id, "Введите комментарий (минимум 10 символов):")
        bot.register_next_step_handler(sent, step_comment)
    else:
        sent = bot.send_message(message.chat.id, "Ошибка: введите ваш email:")
        bot.register_next_step_handler(sent, step_email)


def step_comment(message):
    if not message.text or len(message.text) < 10:
        sent = bot.send_message(message.chat.id, "Ошибка: Комментарий слишком короткий")
        bot.register_next_step_handler(sent, step_comment)
        return
    set_field("comment", message.chat.id, message.text)

    # Получаем данные пользователя
    data = get_user_data(message.chat.id)
    digits, email, comment = data

    # Отправляем админу
    bot.send_message(ADMIN_ID, f"📩 Новая заявка:\nЧисло: {digits}²\nEmail: {email}\nКомментарий: {comment}")

    # Отправляем фото от бота пользователю (здесь нужно указать file_id заранее)
    BOT_PHOTO_ID = "https://static-cse.canva.com/blob/685034/vk1484.png"
    bot.send_photo(message.chat.id, BOT_PHOTO_ID)

    # Сообщение пользователю
    bot.send_message(message.chat.id, "✅ Ваша заявка отправлена! Спасибо за регистрацию.",
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
