from django.shortcuts import render, redirect
from user_profile.forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login

def index(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/index.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:index')  # перенаправление на другую страницу после успешной авторизации
        else:
            # обработка ошибки авторизации
            return render(request, 'registration/login.html', {'error_message': 'Invalid login or password'})
    else:
        return render(request, 'registration/login.html')