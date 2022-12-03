from rest_framework import serializers

from .models import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Delivery
        fields = ['id', 'title', 'price', 'delivery_time_in_hour', 'image', 'date_updated', 'creator']
