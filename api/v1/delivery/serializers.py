from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.urls import reverse

from .models import Delivery


class DeliveryListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedRelatedField(view_name='delivery-detail', read_only=True, source='id')

    class Meta:
        model = Delivery
        fields = [
            'id', 'title', 'price', 'delivery_time_in_hour', 'detail',
            'date_updated', 'available_from_date', 'available_to_date'
        ]


class DeliveryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        exclude = ['id', 'creator', 'creator_detail_on_delete', 'is_active', 'is_deleted', 'date_created']


class DeliveryDashboardListSerializer(DeliveryListSerializer):
    detail = serializers.HyperlinkedRelatedField(view_name='delivery-dashboard-detail', read_only=True, source='id')
    creator_full_name = serializers.CharField(read_only=True, source='get_creator_full_name')
    creator = serializers.URLField(read_only=True, source='get_creator_url')

    class Meta(DeliveryListSerializer.Meta):
        fields = DeliveryListSerializer.Meta.fields + ['creator', 'creator_full_name']

    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['creator'] = self.context['request'].build_absolute_uri('/') + req['creator']
        return req


class DeliveryDashboardRetrieveSerializer(DeliveryDashboardListSerializer):
    class Meta(DeliveryDashboardListSerializer.Meta):
        fields = [
            'title', 'price', 'delivery_time_in_hour', 'info_on_delivery_time',
            'available_from_date', 'available_to_date', 'file', 'image', 'creator',
            'date_created', 'date_updated', 'is_active', 'is_deleted', 'creator_full_name'
        ]

    def validate(self, attrs):
        try:
            Delivery(**attrs).clean()
        except Exception as err:
            raise ValidationError(dict(err))
        return attrs
