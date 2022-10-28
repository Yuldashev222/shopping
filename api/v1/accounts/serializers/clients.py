from rest_framework import serializers, validators
from rest_framework_simplejwt.serializers import PasswordField

from api.v1.accounts import models, enums


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = (
            'phone_number',
            'second_phone_number',
            'email',
            'first_name',
            'last_name',
            'desc',
            'profile_picture',
            'password',
            # 'country_1',
            # 'region_1',
            # 'district_1',
            # 'street_1',
            # 'country_2',
            # 'region_2',
            # 'district_2',
            # 'street_2',
            # 'country_3',
            # 'region_3',
            # 'district_3',
            # 'street_3',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }


class CreateClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }

    def create(self, validated_data):
        role = enums.CustomUserRole.client.value
        return models.Client.objects.create_user(role=role, **validated_data)
