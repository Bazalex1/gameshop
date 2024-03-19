from django.urls import path
from .views import CustomUserDetailView, delete_comment


app_name = "user_profile"

urlpatterns = [
    path('', CustomUserDetailView.as_view(), name='profile_detail'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]
