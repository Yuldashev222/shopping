from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from api.v1.accounts.models import CustomUser, Client
from api.v1.accounts.enums import CustomUserRole
from .all_users import BaseUserRetrieveUpdateSerializer, BaseUserListSerializer


class ClientListSerializer(BaseUserListSerializer):
    class Meta(BaseUserListSerializer.Meta):
        fields = ['id'] + BaseUserListSerializer.Meta.fields


class ClientRegisterSerializer(serializers.ModelSerializer):
    region1 = serializers.CharField(source='get_region_1_display', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'password', 'region_1', 'region1']
        extra_kwargs = {
            'password': {'validators': [validate_password], 'write_only': True},
            'first_name': {'min_length': 4},
            'last_name': {'min_length': 6},
            'region_1': {'write_only': True},
        }

    def create(self, validated_data):
        instance = self.Meta.model.objects.create_user(role=CustomUserRole.client.name, **validated_data)
        return instance


class ClientRetrieveUpdateSerializer(BaseUserRetrieveUpdateSerializer):
    class Meta(BaseUserRetrieveUpdateSerializer.Meta):
        exclude = BaseUserRetrieveUpdateSerializer.Meta.exclude + [
            'last_login', 'creator', 'creator_detail_on_delete', 'is_active', 'is_deleted'
        ]


class OwnerClientRetrieveUpdateSerializer(BaseUserRetrieveUpdateSerializer):
    class Meta(BaseUserRetrieveUpdateSerializer.Meta):
        exclude = BaseUserRetrieveUpdateSerializer.Meta.exclude + [
            'last_login', 'creator', 'creator_detail_on_delete', 'is_active', 'is_deleted'
        ]
