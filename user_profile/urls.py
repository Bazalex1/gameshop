from django.urls import path
from .views import CustomUserDetailView


app_name = "user_profile"

urlpatterns = [
    path('', CustomUserDetailView.as_view(), name='profile_detail'),
]
