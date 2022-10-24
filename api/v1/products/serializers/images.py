from rest_framework import serializers

from api.v1.products.models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductImage
        fields = '__all__'
