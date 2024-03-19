from django.contrib import admin
from .models import Cart, CartItem




class CartAdmin(admin.ModelAdmin):

    list_display = ("user", "created_at")

class CartItemAdmin(admin.ModelAdmin):

    list_display = ("cart", "game", "price", "quantity")

class CartsInline(admin.TabularInline):
    model = Cart
    exclude = ["created_at"]
    extra = 1


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)