from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserChangeForm
from django.shortcuts import redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login

# Create your views here.
class CustomUserDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('registration:login')

    def get_login_url(self):
        return self.login_url + '?next=' + self.request.path

    model = CustomUser
    template_name = 'user_profile/main.html'
    context_object_name = 'CustomUser'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomUserChangeForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            user.refresh_from_db()  # обновляем объект пользователя из базы данных
            login(request, user)  # авторизуем пользователя с новым логином
            return redirect('profile')  # перенаправление на страницу профиля после сохранения
        else:
            print(form.errors)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
