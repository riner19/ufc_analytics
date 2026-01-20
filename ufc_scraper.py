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

    return {
        'Name': name,
        'Reach': metrics.get('Reach', 'N/A'),
        'SLpM': metrics.get('SLpM', '0'),
        'Str_Acc': metrics.get('Str. Acc.', '0%'),
        'TD_Avg': metrics.get('TD Avg.', '0'),
        'TD_Def': metrics.get('TD Def.', '0%')
    }