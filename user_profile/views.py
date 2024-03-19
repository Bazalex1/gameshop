from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomPasswordChangeForm
from django.shortcuts import redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from comments.models import Comment



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
        context['password_form'] = CustomPasswordChangeForm(user=self.request.user)
        context['comments'] = Comment.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if 'save_profile' in request.POST:
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                login(request, user)
                return redirect('user_profile:profile_detail')
            else:
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return self.render_to_response(context)

        if 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                return redirect('user_profile:profile_detail')
            else:
                context = self.get_context_data(**kwargs)
                context['password_form'] = password_form
                return self.render_to_response(context)
            




@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('user_profile:profile_detail')
    comment.delete()
    return redirect('user_profile:profile_detail')