from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission


# Create your models here.

class CustomUser(AbstractUser):
    # добавляем дополнительные поля
    birth_date = models.DateField(null=True, blank=True)

    # измените названия related_name на уникальные
    groups = models.ManyToManyField(Group, verbose_name='groups', related_name='customuser_set', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', related_name='customuser_set', blank=True, help_text='Specific permissions for this user.')