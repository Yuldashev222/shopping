from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    # order = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # product_image_url = serializers.SerializerMethodField(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.CharField(source='product.price', read_only=True)

    class Meta:
        model = OrderItem
        exclude = ['id', 'is_active', 'is_deleted', 'date_updated']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['product', 'order'],
            )
        ]
        # extra_kwargs = {
        #     'order': {'write_only': True},
        # }

    def validate_quantity(self, quantity):
        if quantity < 1:
            raise serializers.ValidationError('quantity must be at least one')

    def validate(self, attrs):
        print(attrs)
        print()
        print()
        print(self)
        # if attrs['quantity'] > attrs['product'].count_in_stock:
        #     raise serializers.ValidationError({'quantity': 'There are not enough products in the warehouse'})
        return attrs

    # def get_product_image_url(self, order_item):
    #     request = self.context.get('context')
    #     url = order_item.product.images.filter(is_main=True)
    #     print(url)
    #     return url
#
#
# class WishlistListRetrieveSerializer(serializers.ModelSerializer):
#     product_image = serializers.ImageField(source='product.images')
#     product_name = serializers.CharField(source='product.name')
#     product_price = serializers.CharField(source='product.price')
#     product_availability = serializers.BooleanField(source='product.count_in_stock')
#     client = serializers.StringRelatedField()
#     client_id = serializers.IntegerField()
#
#     class Meta:
#         model = Wishlist
#         exclude = ['id']
