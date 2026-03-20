import requests
from bs4 import BeautifulSoup


def get_fighter_url(full_name):
    """
    Умный поиск бойца. Обходит баг сайта ufcstats с пробелами.
    Ищет по фамилии, а затем фильтрует таблицу на точное совпадение.
    """
    words = full_name.strip().split()
    if not words:
        return None

    # Берем последнее слово (фамилию) для поиска на сайте
    search_query = words[-1]
    url = f"http://ufcstats.com/statistics/fighters/search?query={search_query}"

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все строки таблицы
        rows = soup.find_all('tr', class_='b-statistics__table-row')

        first_fallback = None

        for row in rows[1:]:  # Пропускаем первую строку (это заголовок таблицы)
            cols = row.find_all('td')
            if len(cols) >= 3:
                first_name = cols[0].text.strip()
                last_name = cols[1].text.strip()
                nickname = cols[2].text.strip()

                a_tag = cols[0].find('a')
                if not a_tag or 'fighter-details' not in a_tag.get('href', ''):
                    continue

                href = a_tag['href']

                # Запоминаем первого бойца из списка на всякий случай
                if not first_fallback:
                    first_fallback = href

                    # Собираем данные из таблицы для проверки
                table_name = f"{first_name} {last_name}".lower()

                # 1. Ищем точное совпадение имени и фамилии
                if full_name.lower() in table_name or table_name in full_name.lower():
                    return href
                # 2. На случай, если юзер ввел только никнейм (например, "Bones")
                if nickname and full_name.lower() in nickname.lower():
                    return href

        # Если точного совпадения нет (например, опечатка), отдаем первого из списка
        return first_fallback
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None


def get_fighter_stats(url):
    """
    Переходит в профиль бойца и собирает его статистику.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    stats = {
        'name': 'Неизвестно',
        'reach': 0.0,
        'slpm': 0.0,  # Акцентированные удары в минуту
        'acc': 0.0  # Точность ударов
    }

    # Достаем реальное имя из профиля
    name_tag = soup.find('span', class_='b-content__title-highlight')
    if name_tag:
        stats['name'] = name_tag.text.strip()

    ul_tags = soup.find_all('ul', class_='b-list__box-list')
    if len(ul_tags) >= 2:
        # 1. Ищем размах рук (Reach) в первой колонке
        for li in ul_tags[0].find_all('li'):
            text = li.text.strip().replace('\n', '').replace('  ', '')
            if 'Reach:' in text:
                reach_str = text.replace('Reach:', '').strip()
                if reach_str not in ['--', '']:
                    try:
                        stats['reach'] = float(reach_str.replace('"', ''))
                    except ValueError:
                        pass

        # 2. Ищем ударную статистику во второй колонке
        for li in ul_tags[1].find_all('li'):
            text = li.text.strip().replace('\n', '').replace('  ', '')
            if 'SLpM:' in text:
                val = text.replace('SLpM:', '').strip()
                try:
                    stats['slpm'] = float(val)
                except ValueError:
                    pass
            elif 'Str. Acc.:' in text:
                val = text.replace('Str. Acc.:', '').strip().replace('%', '')
                try:
                    stats['acc'] = float(val)
                except ValueError:
                    pass

    return stats


def compare_fighters(name1, name2):
    """
    Главная функция: получает ссылки, собирает стату, сравнивает и выдает красивый текст.
    """
    url1 = get_fighter_url(name1)
    url2 = get_fighter_url(name2)

    if not url1:
        return f"❌ Не смог найти бойца по имени: <b>{name1}</b>\nПроверь правильность написания."
    if not url2:
        return f"❌ Не смог найти бойца по имени: <b>{name2}</b>\nПроверь правильность написания."

    f1 = get_fighter_stats(url1)
    f2 = get_fighter_stats(url2)

    real_name1 = f1['name']
    real_name2 = f2['name']

    # --- СРАВНЕНИЕ REACH (РАЗМАХ РУК) ---
    if f1['reach'] == 0 or f2['reach'] == 0:
        reach_text = "Нет полных данных 🤷‍♂️"
    else:
        diff = abs(f1['reach'] - f2['reach'])
        if diff == 0:
            reach_text = "Абсолютно равный 🤝"
        else:
            better = real_name1 if f1['reach'] > f2['reach'] else real_name2
            reach_text = f"У {better} больше (+{diff:.1f}\")"

    # --- СРАВНЕНИЕ ACCURACY (ТОЧНОСТЬ) ---
    if f1['acc'] == 0 or f2['acc'] == 0:
        acc_text = "Нет полных данных 🤷‍♂️"
    else:
        diff = abs(f1['acc'] - f2['acc'])
        if diff == 0:
            acc_text = "Абсолютно равная 🤝"
        else:
            better = real_name1 if f1['acc'] > f2['acc'] else real_name2
            acc_text = f"Лучше у {better} (+{diff:.1f}%)"

    # --- СРАВНЕНИЕ SLpM (ТЕМП УДАРОВ) ---
    if f1['slpm'] == 0 or f2['slpm'] == 0:
        pace_text = "Нет полных данных 🤷‍♂️"
    else:
        diff = abs(f1['slpm'] - f2['slpm'])
        if diff == 0:
            pace_text = "Одинаковый темп 🤝"
        else:
            better = real_name1 if f1['slpm'] > f2['slpm'] else real_name2
            pace_text = f"{better} бьет чаще (+{diff:.2f} акц. ударов/мин)"

    # Формируем финальный HTML-отчет
    report = f"""
🥊 <b>СРАВНЕНИЕ: {real_name1} vs {real_name2}</b>
--------------------------
📏 <b>Размах рук:</b> {reach_text}
🎯 <b>Точность ударов:</b> {acc_text}
👊 <b>Темп боя:</b> {pace_text}
--------------------------
<i>* Данные взяты с официального сайта ufcstats.com</i>
"""
    return report.strip()