from rest_framework import serializers

from api.v1.products.models import Brand


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ['date_created', 'date_updated']
        extra_kwargs = {
            'creator': {'write_only': True},
            'is_active': {'write_only': True, 'default': True},
        }


class ProductBrandDashboardSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.get_full_name', read_only=True)
    creator_id = serializers.IntegerField(source='creator.pk', read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'
        extra_kwargs = {'creator': {'write_only': True}}
