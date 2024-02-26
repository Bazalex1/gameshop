from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.index, name="index"),
    path("game_list", views.game_list, name="game_list"),
    path("shop:<int:game_id>", views.single_game, name="single_game")
]
