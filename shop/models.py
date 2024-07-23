from django.db import models
from django.utils import timezone
from PIL import Image
import os


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Game(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to="game_img", height_field=None, width_field=None, max_length=None)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    rating = models.CharField(max_length=253)
    description = models.CharField(max_length=10000)
    key_qty = models.IntegerField()

    def get_rating_color(self):
        if 'положительные' in self.rating:
            return 'green'
        elif 'Смешанные' in self.rating:
            return 'yellow'
        else:
            return 'red'

    def save(self, *args, **kwargs):
        if self.image:
            # Получаем расширение изображения
            extension = os.path.splitext(self.image.name)[1].lower()

            # Создаем имя изображения на основе заголовка игры
            new_image_name = f"{self.title}{extension}"

            # Обновляем имя изображения перед сохранением
            self.image.name = os.path.join("game_img", new_image_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    