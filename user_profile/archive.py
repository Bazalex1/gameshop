from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser


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
        context['profile'] = self.get_object()
        return context

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('registration:login')

    def get_login_url(self):
        return self.login_url + '?next=' + self.request.path

    model = CustomUser
    fields = ['first_name', 'last_name', 'birth_date']
    template_name = 'user_profile/ProfileUpdateView.html'
    success_url = reverse_lazy('user_profile:profile_detail')

    def get_object(self, queryset=None):
        return self.request.user
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context
