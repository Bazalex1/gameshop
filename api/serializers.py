from shop.models import Game, Category
from rest_framework import serializers, renderers


class GameSerializer(serializers.Serializer):
    title = serializers.CharField()
    created_at = serializers.DateTimeField()
    price = serializers.FloatField()
    image = serializers.ImageField()
    category = serializers.CharField(source='category.title')
    rating = serializers.FloatField()
    description = serializers.CharField()
    key_qty = serializers.IntegerField()

class CategorySerializer(serializers.Serializer):
    title = serializers.CharField()
    created_at = serializers.DateTimeField()

