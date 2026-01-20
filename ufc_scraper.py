import requests
from bs4 import BeautifulSoup

# --- МАСКИРОВКА ---
# Это заставляет сайт думать, что мы заходим с обычного компьютера
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_fighter_url(fighter_name):
    base_url = "http://ufcstats.com/statistics/fighters/search"
    params = {'query': fighter_name}

    # Передаем headers в запрос
    response = requests.get(base_url, params=params, headers=HEADERS)

    if response.status_code != 200:
        print(f"Ошибка сайта: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Получаем все строки таблицы
    rows = soup.find_all('tr', class_='b-statistics__table-row')

    # В поиске ufcstats первые 2 строки могут быть пустыми или заголовками
    # Нам нужно найти первую строку, где есть ссылка на бойца
    for row in rows:
        link = row.find('a', href=True)
        if link:
            return link['href']  # Возвращаем первую найденную ссылку

    return None

def clean_reach(reach_str):
    """
    Превращает "84.5\"" -> 84.5 (float)
    Если данных нет ("--"), возвращает 0
    """
    if reach_str == "--" or reach_str == "N/A":
        return 0.0
    # Убираем кавычку дюйма и пробелы
    clean = reach_str.replace('"', '').strip()
    return float(clean)

def clean_percentage(pct_str):
    """
    Превращает "58%" -> 0.58 (float)
    """
    if pct_str == "--" or pct_str == "N/A":
        return 0.0
    # Убираем знак %
    clean = pct_str.replace('%', '').strip()
    return float(clean) / 100

def get_fighter_data(fighter_url):
    response = requests.get(fighter_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    name_tag = soup.find('span', class_='b-content__title-highlight')
    if not name_tag:
        return None
    name = name_tag.text.strip()

    metrics = {}
    stat_boxes = soup.find_all('li', class_='b-list__box-list-item')

    for box in stat_boxes:
        text = box.text.strip().replace('\n', '').replace('  ', '')
        if ':' in text:
            key, value = text.split(':', 1)
            metrics[key.strip()] = value.strip()

# Извлекаем сырые значения
    raw_reach = metrics.get('Reach', '--')
    raw_slpm = metrics.get('SLpM', '0')
    raw_acc = metrics.get('Str. Acc.', '0%')
    raw_td = metrics.get('TD Avg.', '0')
    raw_td_def = metrics.get('TD Def.', '0%')

    # Возвращаем очищенные данные (числа!)
    return {
            'Name': name,
            'Reach': clean_reach(raw_reach),  # Теперь это float
            'SLpM': float(raw_slpm),  # Просто конвертируем в float
            'Str_Acc': clean_percentage(raw_acc),  # Теперь это 0.XX
            'TD_Avg': float(raw_td),
            'TD_Def': clean_percentage(raw_td_def)
        }