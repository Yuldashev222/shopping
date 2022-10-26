from rest_framework import serializers

from api.v1.products.models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date_created = serializers.DateTimeField(read_only=True, write_only=False)
    date_updated = serializers.DateTimeField(read_only=True, write_only=False)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductImage
        fields = '__all__'
