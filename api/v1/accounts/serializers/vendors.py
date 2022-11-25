from rest_framework import serializers

from api.v1.accounts import models, enums


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = (
            'phone_number',
            'second_phone_number',
            'email',
            'first_name',
            'last_name',
            'desc',
            'profile_picture',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }


class CreateVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'role': {'read_only': True}
        }

    def create(self, validated_data):
        role = enums.CustomUserRole.vendor.name
        return models.Vendor.objects.create_user(role=role, **validated_data)
