from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Game
from comments.forms import CommentForm

# Create your views here.


def index(request):
    games = Game.objects.all()
    return render(request, "shop/main.html", {"games": games})


def game_list(request):
    games = Game.objects.all()
    return render(request, "shop/game_list.html", {"games": games})


def single_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    comments = game.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.game = game
            comment.user = request.user
            comment.save()
            return redirect('shop:single_game', game_id=game_id)
    else:
        form = CommentForm()
    return render(request, "shop/single_game.html", {"game": game,'comments': comments, 'form': form})
