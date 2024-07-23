from django.contrib import admin
from .models import Game, Category
from .forms import GameForm

admin.site.site_header = "Games Admin"
admin.site.site_title = "My games"
admin.site.index_title = "Welcome"

class GameAdmin(admin.ModelAdmin):
    form = GameForm

    list_display = ("title", "price", "category", "rating", "key_qty")

    def save_model(self, request, obj, form, change):
        # Создайте объект Game с предоставленными данными для ручного создания
        obj.title = form.cleaned_data['title']
        obj.price = form.cleaned_data['price']
        obj.category = form.cleaned_data['category']
        obj.rating = form.cleaned_data['rating']
        obj.key_qty = form.cleaned_data['key_qty']
        obj.description = form.cleaned_data['description']
        # Сохраните изображение, если оно предоставлено
        obj.image = form.cleaned_data['image']
        obj.save()

    class Media:
        css = {
            'all': ('styles/admin_style.css',)
        }


class GamesInline(admin.TabularInline):
    model = Game
    exclude = ["created_at"]
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Dates", {
            "fields": ["created_at"],
            "classes": ["collapce"]
        })
    ]
    inlines = [GamesInline]

admin.site.register(Game, GameAdmin)
admin.site.register(Category, CategoryAdmin)
