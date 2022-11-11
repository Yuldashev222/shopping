from rest_framework import serializers

from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_image_url = serializers.SerializerMethodField(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.CharField(source='product.price', read_only=True)
    product_availability = serializers.BooleanField(source='product.count_in_stock', read_only=True)

    class Meta:
        model = Wishlist
        exclude = ['id']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['product', 'client'],
            )
        ]
        extra_kwargs = {
            'product': {'write_only': True},
        }

    def get_product_image_url(self, wishlist):
        request = self.context.get('context')
        url = wishlist.product.images.filter(is_main=True)
        return url


class WishlistListRetrieveSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(source='product.images')
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.CharField(source='product.price')
    product_availability = serializers.BooleanField(source='product.count_in_stock')
    client = serializers.StringRelatedField()
    client_id = serializers.IntegerField()

    class Meta:
        model = Wishlist
        exclude = ['id']
