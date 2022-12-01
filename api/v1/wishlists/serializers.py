from rest_framework import serializers

from .models import Wishlist


class BaseWishlistSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(source='product_item.main_image', read_only=True)
    product_name = serializers.SerializerMethodField(read_only=True)
    product_price = serializers.CharField(source='product_item.price', read_only=True)
    product_availability = serializers.BooleanField(source='product_item.count_in_stock', read_only=True)
    product_item_id = serializers.IntegerField(source='product_item.id', read_only=True)

    def get_product_name(self, wishlist):
        if wishlist.product_item.name:
            return wishlist.product_item.name
        else:
            return wishlist.product_item.product.name

    def get_product_image(self, wishlist):
        request = self.context.get('context')
        image_url = wishlist.product_item.main_image
        return request.build_absolute_uri(image_url)


class WishlistSerializer(BaseWishlistSerializer):
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Wishlist
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['product_item', 'client'],
            )
        ]
        extra_kwargs = {
            'product_item': {'write_only': True},
            'product_image': {'read_only': True},
        }


class WishlistListSerializer(BaseWishlistSerializer):
    product_item_name = serializers.CharField(source='product_item.name')
    product_name = serializers.CharField(source='product_item.product.name')
    client_full_name = serializers.CharField(source='client.get_full_name')
    client_phone_number = serializers.CharField(source='client.phone_number')
    client_email = serializers.CharField(source='client.email')
    client_id = serializers.IntegerField()
    product_id = serializers.IntegerField(source='product_item.product.id')

    class Meta:
        model = Wishlist
        exclude = ['id', 'product_item', 'client']
