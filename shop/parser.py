import tempfile
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

# Парсер для получения данных с сайта cupicod в  словарь product_info по ключам 'title','description','price','rating'.
# А также с возможностью скачать изображение.


def parse_product_page(url):
    # Отправляем GET-запрос к странице магазина
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        title = None
        description = None
        price = None
        rating = None

         # Создаем экземпляр драйвера браузера
        driver = webdriver.Chrome()

        # Открываем страницу игры
        driver.get(url)
        try:
            # Ждем, пока загрузится страница
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.modal-content.popunder')))
        except:
            print("первая загруза")
            # Закрываем рекламную плашку
        try:

            driver.execute_script("""
                // Находим элемент "Закрыть"
                var close = document.querySelector('.modal__close');

                // Кликаем по элементу "Закрыть"
                close.click();
            """)
        except:
            print("закрытие плашки")
        try:
            # Ждем, пока загрузится страница
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.switch_tab')))
        except:
            print("вторая загруза")
        # Находим элемент "Описание" по его содержимому
        tab = driver.find_element(By.XPATH, "//div[contains(text(), 'Описание')]")

        # Кликаем по элементу "Описание"
        tab.click() 

        try:
            title = soup.find(
                'h1', class_='max-mobile:hidden').text.strip()
        except:
            print("Ошибка при парсинге названия")
        # Ждем, пока загрузится описание
            
        time.sleep(3)
        # Находим элемент описания
        description_elements = driver.find_element(By.CSS_SELECTOR, '.tab-desc-content')
        print(description_elements)

        # Проверяем, что элемент был найден
        try:
            if description_elements:
                # Получаем описание игры
                description = description_elements.get_attribute('textContent')
                print(description)
            else:
                print("Элемент 'Описание' не был найден")
        except:
            print("АШИБКА Элемент 'Описание' не был найден")

        # Это было без драйваера try:
        #     # Ваш код парсинга описания игры
        #     description = soup.find('div', class_='tab-desc-content').get_text(strip=True)
        #     print("Описание игры:", description)
        #     return description
        # except Exception as e:
        #     print("Ошибка при парсинге описания:", e)
        
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

        # Получаем URL изображения
        image_url = extract_image_url_from_url(url)

        # Скачиваем изображение
        downloaded_image_file_name = download_image(image_url)

        # Открываем скачанное изображение в режиме чтения
        with open(downloaded_image_file_name, 'rb') as f:
            # Создаем объект ContentFile из изображения
            image_content_file = ContentFile(f.read())

        # Создаем объект ImageFile из ContentFile
        image_file = ImageFile(image_content_file, name='image.jpg')

        driver.quit()

        # Добавляем изображение в словарь product_info
        product_info = {
            'title': title,
            'description': description,
            'price': price,
            'rating': rating,
            'image': image_file
        }

        return product_info

    else:
        print("Ошибка при загрузке страницы")
        return None


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(response.content)
            return f.name.encode('utf-8')
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
