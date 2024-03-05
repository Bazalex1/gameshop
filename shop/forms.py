from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    url = forms.URLField(label='URL игры', widget=forms.URLInput(attrs={'class': 'form-control'}))
    number_of_keys = forms.IntegerField(label='Число ключей для продажи', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Game
        fields = ('url', 'number_of_keys')