from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser


class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'CustomUser_detail.html'
    context_object_name = 'CustomUser'

    def get_object(self, queryset=None):
        return self.request.user.CustomUser

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'birth_date']
    template_name = 'CustomUser_edit.html'
    success_url = reverse_lazy('CustomUser_detail')

    def get_object(self, queryset=None):
        return self.request.user.CustomUser
# Create your views here.
