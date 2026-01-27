import pandas as pd
from ufc_scraper import get_fighter_data, get_fighter_url


def compare_fighters(name1, name2):
    """
    1. Finds links to fighters.
    2. Downloads fighters' data.
    3. Compares fighters' data by pandas dataframe.
    4. Returns report for telegram.
    """

    # 1. Получаем ссылки на профили
    url1 = get_fighter_url(name1)
    url2 = get_fighter_url(name2)

    # Если кого-то не нашли — возвращаем ошибку
    if not url1 or not url2:
        return f"❌ Unable to find the fighters. Check the names: {name1}, {name2}"

    # 2. Скачиваем данные (используем наш ufc_scraper)
    data1 = get_fighter_data(url1)
    data2 = get_fighter_data(url2)

    if not data1 or not data2:
        return "❌ ERROR GETTING THE DATA."

    # 3. АНАЛИТИКА ЧЕРЕЗ PANDAS
    # Создаем таблицу из двух бойцов
    df = pd.DataFrame([data1, data2])

    # Делаем имена "заголовками" строк
    df.set_index('Name', inplace=True)

    # Считаем разницу (Боец 2 - Боец 1).
    # diff() вычитает предыдущую строку из текущей.
    # iloc[-1] берет последнюю строку (результат вычитания).
    difference = df.diff().iloc[-1]

    # 4. Формируем красивый отчет текстом
    report = f"🥊 <b>COMPARISON: {data1['Name']} vs {data2['Name']}</b>\n"
    report += "--------------------------\n"

    # Сравниваем Reach (Размах рук)
    reach_diff = difference['Reach']
    if reach_diff > 0:
        report += f"📏 <b>Reach:</b> {data2['Name']} (+{abs(reach_diff):.1f}\")\n"
    elif reach_diff < 0:
        report += f"📏 <b>Reach:</b> {data1['Name']} (+{abs(reach_diff):.1f}\")\n"
    else:
        report += f"📏 <b>Reach:</b> Same ({data1['Reach']}\")\n"

    # Сравниваем Точность ударов (Str_Acc)
    # Умножаем на 100, чтобы показать проценты
    acc_diff = difference['Str_Acc'] * 100
    if acc_diff > 0:
        report += f"🎯 <b>Accuracy:</b> {data2['Name']} better by {abs(acc_diff):.1f}%\n"
    elif acc_diff < 0:
        report += f"🎯 <b>Accuracy:</b> {data1['Name']} better by {abs(acc_diff):.1f}%\n"

    # Сравниваем Удары в минуту (SLpM)
    slpm_diff = difference['SLpM']
    if slpm_diff > 0:
        report += f"👊 <b>Movement pace:</b> {data2['Name']} punches more frequently  (+{abs(slpm_diff):.1f}/мин)\n"
    elif slpm_diff < 0:
        report += f"👊 <b>Movement pace:</b> {data1['Name']} puncher more frequently (+{abs(slpm_diff):.1f}/мин)\n"

    report += "--------------------------\n"
    report += "<i>All of the data from ufcstats.com</i>"

    return report


# --- ТЕСТ (если запускать файл отдельно) ---
if __name__ == "__main__":
    print(compare_fighters("Jon Jones", "Tom Aspinall"))