from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from api.v1.accounts.models import CustomUser, Director
from api.v1.accounts.enums import CustomUserRole
from .all_users import BaseUserRetrieveUpdateSerializer, BaseUserListSerializer, UserRetrieveUpdateSerializer


class StaffRegisterSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    re_password = serializers.CharField(write_only=True, label='reply password', style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = [
            'phone_number', 'second_phone_number', 'email', 'first_name', 'last_name',
            'password', 're_password', 'region_1', 'role', 'creator', 'is_active'
        ]
        extra_kwargs = {
            'password': {'validators': [validate_password], 'write_only': True, 'style': {'input_type': 'password'}},
            'first_name': {'min_length': 4},
            'last_name': {'min_length': 6},
        }

    def validate_role(self, role):

        if role == CustomUserRole.client.name:
            raise ValidationError(f'"{role}" is not a valid choice.')

        if role == CustomUserRole.director.name and Director.objects.exists():
            raise ValidationError('director must be unique')

        return role

    def validate(self, attrs):
        role = attrs['role']
        creator = attrs['creator']

        if (
                role in [CustomUserRole.developer.name, CustomUserRole.director.name]
                and
                creator.role != CustomUserRole.developer.name

                or

                role == CustomUserRole.manager.name
                and
                creator.role not in [CustomUserRole.developer.name, CustomUserRole.director.name]

                or

                role == CustomUserRole.vendor.name
                and
                creator.role in [CustomUserRole.vendor.name, CustomUserRole.client.name]
        ):
            raise ValidationError(f'You do not have permission to register the "{role}" role.')

        if attrs['re_password'] != attrs['password']:
            raise ValidationError({'re_password': ['passwords are not the same']})
        return attrs

    def create(self, validated_data):
        del validated_data['re_password']
        validated_data['password'] = make_password(validated_data['password'])
        instance = self.Meta.model.objects.create(is_staff=True, **validated_data)
        return instance


class OwnerStaffRetrieveUpdateSerializer(UserRetrieveUpdateSerializer):
    creator = None

    class Meta(UserRetrieveUpdateSerializer.Meta):
        exclude = UserRetrieveUpdateSerializer.Meta.exclude + [
            'is_active', 'is_deleted', 'creator', 'creator_detail_on_delete', 'last_login'
        ]

    def to_representation(self, instance):
        return super(BaseUserRetrieveUpdateSerializer, self).to_representation(instance)


class StaffListSerializer(BaseUserListSerializer):
    position = serializers.CharField(source='get_role_display', read_only=True)

    class Meta(BaseUserListSerializer.Meta):
        fields = ['id', 'position', 'role', 'photo'] + BaseUserListSerializer.Meta.fields

    def to_representation(self, instance):
        request_user_role = self.context['request'].user.role
        ret = super(StaffListSerializer, self).to_representation(instance)
        if (
                request_user_role == CustomUserRole.vendor.name
                or
                request_user_role == ret['role']
                or
                request_user_role == CustomUserRole.manager.name and ret['role'] == CustomUserRole.director.name
        ):
            del ret['is_active'], ret['is_deleted']
        del ret['role']
        return ret
