import telebot
import os
import time
from dotenv import load_dotenv
from analytics import compare_fighters

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
        "Use command: /compare [Боец1] [Боец2]\n\n"
        "For expample: /compare Jones Aspinall"
    )
    bot.reply_to(message, welcome_text)


# --- /compare ---
@bot.message_handler(commands=['compare'])
def handle_compare(message):
    # Message looks like: "/compare Jones Aspinall"
    # Parsing it to words
    parts = message.text.split()

    # Check if 2 fighters typed?
    if len(parts) < 3:
        bot.reply_to(message, "⚠️ Ошибка! Нужно ввести два имени.\nПример: /compare Jones Aspinall")
        return

    # Getting names (skip[0], because its command istels /compare)
    fighter1 = parts[1]
    fighter2 = parts[2]

    bot.reply_to(message, f"🔍 Searching: {fighter1} vs {fighter2}...\nЭто может занять пару секунд.")

    # Analytics (from analytics.py)
    try:
        report = compare_fighters(fighter1, fighter2)
        # sending result
        bot.send_message(message.chat.id, report)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при анализе: {e}")


if __name__ == "__main__":
    print("🤖 Bot is launched!...")
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=5)
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)