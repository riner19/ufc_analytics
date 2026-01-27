import telebot
import os
from dotenv import load_dotenv # Импортируем загрузчик
from analytics import compare_fighters

# Загружаем переменные из файла .env
load_dotenv()

# Берем токен из переменных окружения (безопасно!)
API_TOKEN = os.getenv('BOT_TOKEN')

if not API_TOKEN:
    print("Error: TOKEN not found! Check file .env")
    exit()

bot = telebot.TeleBot(API_TOKEN)


print("✅ Bot is launched and ready to work...")


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


# --- Обработка команды /compare ---
@bot.message_handler(commands=['compare'])
def handle_compare(message):
    # Сообщение выглядит так: "/compare Jones Aspinall"
    # Нам нужно разбить его на слова
    parts = message.text.split()

    # Проверка: ввел ли пользователь два имени?
    if len(parts) < 3:
        bot.reply_to(message, "⚠️ Ошибка! Нужно ввести два имени.\nПример: /compare Jones Aspinall")
        return

    # Берем имена (пропускаем parts[0], т.к. это сама команда /compare)
    fighter1 = parts[1]
    fighter2 = parts[2]

    bot.reply_to(message, f"🔍 Ищу данные: {fighter1} vs {fighter2}...\nЭто может занять пару секунд.")

    # Вызываем нашу аналитику (из файла analytics.py)
    try:
        report = compare_fighters(fighter1, fighter2)
        # Отправляем результат
        bot.send_message(message.chat.id, report)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при анализе: {e}")


# --- Запуск бесконечного цикла (чтобы бот не выключался) ---
bot.infinity_polling()