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


serializer_obj = GameSerializer(instance=Game.objects.all(), many=True)
json_render_for_our_data = renderers.JSONRenderer()
data_in_json = json_render_for_our_data.render(serializer_obj.data)
