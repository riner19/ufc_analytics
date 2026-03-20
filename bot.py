import telebot
import os
import time
from dotenv import load_dotenv
from analytics import compare_fighters
from database import init_db, log_search
# getting variable from .env
load_dotenv()

# Getting token
API_TOKEN = os.getenv('BOT_TOKEN')

if not API_TOKEN:
    print("Error: TOKEN not found! Check file .env")
    exit()

bot = telebot.TeleBot(API_TOKEN)



# --- command /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Hello! I am UFC Analytics Bot.\n\n"
        "I can compare fighters statistics.\n"
        "Use command: /compare [Боец1], [Боец2]\n\n"
        "For expample: /compare Jon Jones, Tom Aspinall (with full names)."
    )
    bot.reply_to(message, welcome_text)


# --- /compare ---
@bot.message_handler(commands=['compare'])
def handle_compare(message):
    # Убираем команду из текста и разбиваем по запятой
    text = message.text.replace('/compare', '').strip()
    parts = text.split(',')

    # Проверяем, что есть ровно два бойца, разделенных запятой
    if len(parts) != 2:
        bot.reply_to(message, "⚠️ Ошибка! Введи полные имена бойцов через запятую.\nПример: /compare Jon Jones, Tom Aspinall")
        return

    # Очищаем от лишних пробелов по краям
    fighter1 = parts[0].strip()
    fighter2 = parts[1].strip()

    user_id = message.from_user.id
    username = message.from_user.username
    log_search(user_id, username, fighter1, fighter2)

    bot.reply_to(message, f"🔍 Сравниваю: {fighter1} vs {fighter2}...\nЭто может занять пару секунд.")

    try:
        report = compare_fighters(fighter1, fighter2)
        bot.send_message(message.chat.id, report, parse_mode="HTML") # Добавили HTML для красоты
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при анализе: {e}")


if __name__ == "__main__":
    # 1. creating table first
    init_db()

    # 2. start infinity loop
    bot.infinity_polling(timeout=60, long_polling_timeout=5)