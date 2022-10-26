from rest_framework import serializers

from api.v1.products.models import ProductStar


class ProductStarSerializer(serializers.ModelSerializer):
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductStar
        fields = '__all__'
