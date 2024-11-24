from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from comments.forms import CommentForm
from django.contrib import messages

# Create your views here.


def index(request):
    # Список из 5 игр, которые вы хотите отобразить на главной странице
    featured_games = Game.objects.filter(id__in=[1, 2, 3, 4, 5])
    context = {'featured_games': featured_games}
    return render(request, 'shop/main.html', context)


def game_list(request):
    games = Game.objects.all()
    return render(request, "shop/game_list.html", {"games": games})


def single_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    comments = game.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.game = game
                comment.user = request.user
                comment.save()
                messages.success(request, 'Комментарий успешно добавлен.')
                return redirect('shop:single_game', game_id=game_id)
        else:
            messages.error(request, 'Для добавления комментария вам нужно войти в систему.')
            return redirect('login')  # Перенаправление на страницу входа

    else:
        form = CommentForm()

    return render(request, "shop/single_game.html", {"game": game, 'comments': comments, 'form': form})
