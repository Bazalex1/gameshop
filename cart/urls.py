from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('', views.cart, name="index"),
    path('add_to_cart/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('key', views.get_key, name="key"),
]
