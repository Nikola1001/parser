import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-jeep/'
#URL = 'https://auto.ria.com/newauto/marka-lifan/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36', 'accept': '*/*'} #Заголовки защита от ботов
HOST='https://auto.ria.com'
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers= HEADERS, params=params)
    return r

def get_pages_counter(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1




def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition_area')
    # print(items)

    cars=[]
    for item in items:
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True), #заголовок класса... и удаление пробелов в нач и конц
            'link': HOST + item.find('a').get('href'),  #атрибут в ссылке
            'price': item.find('div', class_='proposition_price').find_next('span').get_text(),
            'city' : item.find('div', class_='proposition_region grey size13').find_next('strong').get_text(),
        })
    return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['city']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars=[]
        pages_count=get_pages_counter(html.text)

        for page in range(1, pages_count+1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')
        os.startfile(FILE)
    else:
        print('Error')
        print(html)

parse()
