from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Game

# Create your views here.


def index(request):
    games = Game.objects.all()
    return render(request, "shop/main.html", {"games": games})


def game_list(request):
    games = Game.objects.all()
    return render(request, "shop/game_list.html", {"games": games})


def single_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, "shop/single_game.html", {"game": game})
