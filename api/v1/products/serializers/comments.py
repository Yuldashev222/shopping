from rest_framework import serializers

from api.v1.products.models import ProductComment


class ProductCommentSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(default=serializers.CurrentUserDefault())
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductComment
        fields = '__all__'
