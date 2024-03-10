from django.shortcuts import render, redirect
from user_profile.forms import CustomUserCreationForm

def index(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/index.html', {'form': form})
