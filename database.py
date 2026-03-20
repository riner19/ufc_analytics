import sqlite3
import datetime
import os

os.makedirs('data', exist_ok=True)

# Подключаемся к базе (если файла нет, Python сам его создаст)
conn = sqlite3.connect('ufc_bot.db', check_same_thread=False)
cursor = conn.cursor()

def init_db():
    """CREATING TABLE IF IT NOT EXISTS"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            fighter1 TEXT,
            fighter2 TEXT,
            search_date TIMESTAMP
        )
    ''')
    conn.commit()
    print("DATABASE CREATED.")

def log_search(user_id, username, fighter1, fighter2):
    """ADDING DATA TO TABLE"""
    now = datetime.datetime.now()
    cursor.execute('''
        INSERT INTO search_history (user_id, username, fighter1, fighter2, search_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, fighter1, fighter2, now))
    conn.commit()

# При запуске этого файла база данных будет создана
if __name__ == "__main__":
    init_db()