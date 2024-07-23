from django.db import models
from user_profile.models import CustomUser
from shop.models import Game

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart for user {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.game.title} in cart for user {self.cart.user.username}'
    
class Key(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # Связываем ключ с игрой
    created_at = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=255)  # Убедитесь, что поле key это CharField

    def __str__(self):
        return f'{self.key} for {self.user.username}'
