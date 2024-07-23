from django import forms
from .models import Game, Category

class GameForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', widget=forms.Select(attrs={'class': 'form-control'}))
    key_qty = forms.IntegerField(label='Число ключей для продажи', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label='Название',required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Цена',required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    rating = forms.CharField(label='Рейтинг',required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    image = forms.ImageField(label='Изображение', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Game
        fields = ('key_qty', 'category', 'title', 'price', 'rating','description', 'image')
