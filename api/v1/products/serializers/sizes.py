from rest_framework import serializers

from api.v1.products.models import ProductSize


class ProductSizeSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductSize
        fields = '__all__'
