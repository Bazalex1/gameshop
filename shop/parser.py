from tempfile import TemporaryFile
import requests
from bs4 import BeautifulSoup
import re
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid
from django.core.files.base import ContentFile
from decimal import Decimal

# Парсер для получения данных с сайта cupicod в  словарь product_info по ключам 'title','description','price','rating', 'image.
# А также с возможностью скачать изображение.

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def parse_product_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Безголовой режим
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")

    service = Service('/usr/local/bin/chromedriver')  # Путь к ChromeDriver

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    try:
        # Ждем, пока загрузится страница
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.modal-content.popunder')))
    except:
        print("первая загрузка")

    try:
        driver.execute_script("""
            var close = document.querySelector('.modal__close');
            close.click();
        """)
    except:
        print("закрытие плашки")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.switch_tab')))
    except:
        print("вторая загрузка")

    tab = driver.find_element(By.XPATH, "//div[contains(text(), 'Описание')]")
    tab.click()

    time.sleep(1)
    description_elements = driver.find_element(By.CSS_SELECTOR, '.tab-desc-content')
    description = description_elements.get_attribute('textContent') if description_elements else None

    title = None
    pre_price = None
    rating = None

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup.find('h1', class_='max-mobile:hidden').text.strip()
        pre_price = soup.find('span', class_='product_region-select-text_price').text.strip()
        rating = soup.find('div', class_='game-ext-data__line').text.strip()
    except:
        print("Ошибка при парсинге")

    image_url = extract_image_url_from_url(url)
    image_file = download_image(image_url)
    
    driver.quit()
    
    cleaned_price_string = re.sub(r'[^\d.]', '', pre_price)
    price = Decimal(cleaned_price_string)

    product_info = {
        'title': title,
        'description': description,
        'price': price,
        'rating': rating,
        'image': image_file
    }

    return product_info

# Другие ваши функции




def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Создаем уникальное имя файла
        file_name = f'{uuid.uuid4()}.jpg'

        # Сохраняем изображение в памяти
        content = ContentFile(response.content)

        # Создаем экземпляр ImageFieldFile
        image_file = ImageFile(content, name=file_name)

        # Возвращаем экземпляр ImageFieldFile
        return image_file
    else:
        print("Ошибка при загрузке картинки")
        return None



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
            print("URl Картинки получен")
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
