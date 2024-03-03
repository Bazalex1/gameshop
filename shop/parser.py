import requests
from bs4 import BeautifulSoup
import re

# Парсер для получения данных с сайта cupicod в  словарь product_info по ключам 'title','description','price','rating'.
# А также с возможностью скачать изображение.


def parse_product_page(url):
    # Отправляем GET-запрос к странице магазина
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим элементы с информацией о товаре
        try:
            title = soup.find(
                'h1', class_='max-mobile:hidden').text.strip()
        except:
            print("Ошибка при парсинге названия")
        try:
            description = soup.find(
                'div', class_='tab-desc-content').text.strip()
        except:
            print("Ошибка при парсинге описания")
        try:
            price = soup.find(
                'span', class_='product_region-select-text_price').text.strip()
        except:
            print("Ошибка при парсинге цены")
        try:
            rating = soup.find(
                'div', class_='game-ext-data__line').text.strip()
        except:
            print("Ошибка при парсинге рейтинга")
        return {
            'title': title,
            'description': description,
            'price': price,
            'rating': rating,
        }

    else:
        print("Ошибка при загрузке страницы")
        return None


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("Картинка успешно скачана")
    else:
        print("Ошибка при загрузке картинки")


def extract_image_url_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Находим элемент, содержащий атрибут style
    image_element = soup.find('div', class_='product_image relative')
    if image_element:
        # Получаем значение атрибута style
        style = image_element.get('style', '')
        # Используем регулярное выражение для извлечения URL из атрибута style
        match = re.search(r"url\(['\"]?([^'\")]+)['\"]?\)", style)
        if match:
            return match.group(1)
    else:
        print("ошибка получения изображения")
    return None


# # сюда вставлять ссылку на kupicod
# product_url = ''


# product_info = parse_product_page(product_url)
# if product_info:
#     print(product_info)
# else:
#     print("Не удалось получить информацию о товаре")


# image_url = extract_image_url_from_url(product_url)

# if image_url:
#     print("URL изображения:", image_url)
#     # Укажите имя файла для сохранения
#     download_image(image_url, product_info["title"] + ".jpg")
# else:
#     print("Не удалось извлечь URL изображения")


# # # Законсервированный код с функционалом получения рейтинга с сайта metacritic свернут по причине низвестной пробелемы с получением get запроса( Error: read ECONNRESET)
# # функция для получения названия игры для поиска на metacritic
# def get_substring_past_last_slash(input_string):
#     index = input_string.rfind('/')
#     return input_string[index:]


# url_metacritic = "https://www.metacritic.com/game" + \
#     get_substring_past_last_slash(product_url)
# print(url_metacritic)


# def parse_product_metacritic(url):
#     # Отправляем GET-запрос к странице магазина
#     response = requests.get(url)
#     # Проверяем успешность запроса
#     if response.status_code == 200:
#         # Создаем объект BeautifulSoup для парсинга HTML
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Находим элементы с информацией о товаре
#         rating = soup.find(
#             'span', class_='data-v-4cdca868').text.strip()

#     else:
#         print("Ошибка при загрузке страницы metacritic")
#         return None

#     return rating


# metacritic_rate = parse_product_metacritic(url_metacritic)
# print(metacritic_rate)
