from rest_framework import serializers

from api.v1.products.models import ProductColor


class ProductColorSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductColor
        fields = '__all__'
