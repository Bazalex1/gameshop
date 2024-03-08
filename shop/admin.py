from django.core.files.base import ContentFile
from django.contrib import admin
from .forms import GameForm
from .models import Game
from .parser import extract_image_url_from_url, download_image, parse_product_page
import os
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import tempfile
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files import File
from io import BytesIO
import re



class GameAdmin(admin.ModelAdmin):
    form = GameForm  # Установите вашу форму

    def save_model(self, request, obj, form, change):
        if not change:  # Если это новая запись, а не изменение существующей
            url = form.cleaned_data['url']  # Получите URL из формы
            number_of_keys = form.cleaned_data['key_qty']  # Получите число ключей из формы
            category = form.cleaned_data['category']  # Получите категорию из формы
            data = parse_product_page(url)  # Вызовите ваш парсер
            data['key_qty'] = number_of_keys  # Добавьте число ключей в данные
            data['category'] = category  # Добавьте категорию в данные
            obj = Game.objects.create(**data)  # Создайте новый объект Game
        else:
            super().save_model(request, obj, form, change)

admin.site.register(Game, GameAdmin)