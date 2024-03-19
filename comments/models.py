from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Game
from django.utils import timezone


class Comment(models.Model):
# Create your models here.
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
