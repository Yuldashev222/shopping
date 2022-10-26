from datetime import date
from rest_framework import serializers

from api.v1.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_id = serializers.IntegerField()
    date_created = serializers.DateTimeField(read_only=True, write_only=False)
    date_updated = serializers.DateTimeField(read_only=True, write_only=False)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = '__all__'
