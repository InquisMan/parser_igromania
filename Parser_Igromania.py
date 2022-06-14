import requests  # для работы с запросами
from bs4 import BeautifulSoup  # для парсинга
import csv  # для работы с excel-файлами
import os  # для работы с Windows


CSV = 'game_cards.csv'  # создание excel-файла для собранной информации
HOST = 'https://igromania.ru/'  # адрес сайта
HOST2 = 'https:'  # позволяет добавить протокол к тем адресам, где он отсутствует
page = 1  # переменная, содержащая номер страницы
URL = f'https://www.igromania.ru/games/all/all/all/all/all/0/{page}'  # полный адрес с указанием на искомое содержимое


HEADERS = {  # переменная, содержащая заголовки
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
}


def get_html(url):  # функция, которая позволяет получить html-код сайта
    r = requests.get(url, headers=HEADERS)  # запрос на страницу, где забирается html-код

    return r


def get_content(html):  # функция, которая принимает html, с которым мы работаем
    soup = BeautifulSoup(html, 'html.parser')  # модуль парсинга
    items = soup.find_all('div', class_='game-card')  # сбор всех элементов из блока
    game_cards = []  # создание списка всех искомых элементов

    for item in items:  # цикл для нахождения конкретных элементов и сбора их в список 'game_cards'
        game_cards.append(
            {
                'title': item.find('a', class_='name').get_text(strip=True),
                'link_game': HOST + item.find('div', class_='left-block').find('a').get('href'),
                'platforms': item.find('div', class_='platforms').get_text(strip=True),
                'tags': item.find('div', class_='tags').get_text(strip=True),
                'game_image': HOST2 + item.find('img', class_='image').get('src'),
                'metacritic_rating': item.find('div', class_='metacritic').find('div', class_='text').get_text(strip=True),
            }
        )
    return game_cards


def save_doc(items, path):  # функция, которая сохраняет полученную информацию в документ формата .csv
    with open(path, 'w', newline='') as file:  # функция, открывающая файл для записи
        writer = csv.writer(file, delimiter=';')  # создание и запись данных в файл CSV
        writer.writerow(['Название игры', 'Ссылка на статью', 'Платформы', 'Тэги', 'Картинка игры',
                         'Оценка с Metacritic'])  # запись строк в файловые объекты, создание заголовков столбцов
        for item in items:
            writer.writerow([item['title'], item['link_game'], item['platforms'], item['tags'], item['game_image'],
                             item['metacritic_rating']])  # распределение элементов по столбцам


def start_parser():  # главная функция запуска парсера
    global page, URL  # объявление переменных видимыми для этой функции
    print('Парсер от Евгения Дорожкина')
    p1 = int(input('Введите первую страницу парсинга: '))
    p2 = int(input('Введите последнюю страницу парсинга: '))
    html = get_html(URL)  # переменная, содержащая код страницы, вызванный функцией "get_html"
    if html.status_code == 200:  # проверка на положительный ответ сервера
        game_cards = []
        page = p1
        URL = f'https://www.igromania.ru/games/all/all/all/all/all/0/{page}'
        for page in range(p1, p2 + 1):  # цикл пагинации
            print(f'Parsing the page: {page}')
            print(URL)
            html = get_html(URL)
            game_cards.extend(get_content(html.text))  # расширенный список, принимающий все элементы страницы
            save_doc(game_cards, CSV)  # сохранение содержимого в CSV-файл
            print(page)
            page += 1
            URL = f'https://www.igromania.ru/games/all/all/all/all/all/0/{page}'

        print('Parsing stopped')
        print('Вся информация собрана в excel-документе, хотите открыть его? да/нет')
        x = str(input('Введите команду: '))
        if x == 'да':
            os.startfile(os.path.abspath('game_cards.csv'))
        else:
            print('Программа закончила свою работу')
    else:
        print('Error')


start_parser()
