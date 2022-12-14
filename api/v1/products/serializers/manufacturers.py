from rest_framework import serializers

from api.v1.products.models import ProductManufacturer


class ProductManufacturerSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date_created = serializers.DateTimeField(read_only=True, write_only=False)
    date_updated = serializers.DateTimeField(read_only=True, write_only=False)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductManufacturer
        fields = '__all__'
