from rest_framework import serializers

from api.v1.accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password', 'is_staff', 'is_superuser', 'user_permissions', 'groups', 'is_active']
