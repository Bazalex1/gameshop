from django.core.files.base import ContentFile
from django.contrib import admin
from .forms import GameForm
from .models import Game
from .parser import extract_image_url_from_url, download_image, parse_product_page
import os


class GameAdmin(admin.ModelAdmin):
    form = GameForm  # Установите вашу форму

    def save_model(self, request, obj, form, change):
        if not change:  # Если это новая запись, а не изменение существующей
            url = form.cleaned_data['url']  # Получите URL из формы
            number_of_keys = form.cleaned_data['number_of_keys']  # Получите число ключей из формы
            data = parse_product_page(url)  # Вызовите ваш парсер
            data['number_of_keys'] = number_of_keys  # Добавьте число ключей в данные

            # Получите URL изображения
            image_url = extract_image_url_from_url(url)
            if image_url:
                # Скачайте изображение
                temp_file_name = download_image(image_url)
                if temp_file_name:
                    # Создайте ContentFile из временного файла
                    content_file = ContentFile(open(temp_file_name, 'rb').read())
                    # Создайте имя файла для сохранения
                    file_name = os.path.basename(temp_file_name)
                    # Сохраните ContentFile в поле ImageField
                    data['image'] = ContentFile(content_file, file_name)

            obj = Game.objects.create(**data)  # Создайте новый объект Game
        else:
            super().save_model(request, obj, form, change)
            
admin.site.register(Game, GameAdmin)