# Импортируем наши функции из соседнего файла
from ufc_scraper import get_fighter_url, get_fighter_data
import pandas as pd


# Тест работы программы
def test_system():
    # 1. Спрашиваем имя (симуляция ввода пользователя)
    target_name = "Khabib"
    print(f"🔍 Fighter to look for: {target_name}...")

    # 2. Ищем ссылку
    url = get_fighter_url(target_name)

    if url:
        print(f"✅ Link found: {url}")

        # 3. Достаем статистику
        data = get_fighter_data(url)

        # 4. Показываем результат
        df = pd.DataFrame([data])
        print("\n📊 fighter Statistics:")
        print(df.to_string(index=False))  # to_string убирает лишние индексы при печати
    else:
        print("❌ Fighter not found.")


if __name__ == "__main__":
    test_system()