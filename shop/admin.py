from django.core.files.base import ContentFile
from django.contrib import admin
from .forms import GameForm
from .models import Game
from .parser import extract_image_url_from_url, download_image, parse_product_page
import os
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import tempfile


class GameAdmin(admin.ModelAdmin):
    form = GameForm  # Установите вашу форму

    def save_model(self, request, obj, form, change):
        if not change:  # Если это новая запись, а не изменение существующей
            url = form.cleaned_data['url']  # Получите URL из формы
            number_of_keys = form.cleaned_data['key_qty']  # Получите число ключей из формы
            data = parse_product_page(url)  # Вызовите ваш парсер
            data['key_qty'] = number_of_keys  # Добавьте число ключей в данные

             # Получите изображение из данных
            image_file = data.pop('image', None)
            if image_file:
                # Прочитайте содержимое объекта ImageFile в байтовую строку
                image_bytes = image_file.read()
                
                # Создайте объект InMemoryUploadedFile из байтовой строки
                image_content = io.BytesIO(image_bytes)
                obj.image.save(image_file.name, InMemoryUploadedFile(
                    image_content, None, image_file.name, 'image/jpeg', len(image_bytes), None))
            

            obj = Game.objects.create(**data)  # Создайте новый объект Game
        else:
            super().save_model(request, obj, form, change)

admin.site.register(Game, GameAdmin)