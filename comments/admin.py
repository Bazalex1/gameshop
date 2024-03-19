from django.contrib import admin
from .models import Comment
from .forms import CommentForm




class CommentAdmin(admin.ModelAdmin):
    form = CommentForm

    list_display = ("user", "text", "game", "created_at")

class CommentsInline(admin.TabularInline):
    model = Comment
    exclude = ["created_at"]
    extra = 1


admin.site.register(Comment, CommentAdmin)