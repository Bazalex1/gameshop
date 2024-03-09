from django.urls import path
from .views import CustomUserDetailView, CustomUserUpdateView


app_name = "user_profile"

urlpatterns = [
    path('', CustomUserDetailView.as_view(), name='profile_detail'),
    path('edit/', CustomUserUpdateView.as_view(), name='profile_edit'),
]
