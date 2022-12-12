from rest_framework import serializers

from api.v1.accounts.models import CustomUser, UserDetailOnDelete


class BaseUserRetrieveUpdateSerializer(serializers.ModelSerializer):
    region1 = serializers.CharField(source='get_region_1_display', read_only=True)
    region2 = serializers.CharField(source='get_region_2_display', read_only=True)
    region3 = serializers.CharField(source='get_region_3_display', read_only=True)

    class Meta:
        model = CustomUser
        exclude = [
            'id', 'is_superuser', 'groups', 'user_permissions',
            'date_updated', 'password', 'is_staff', 'role'
        ]
        extra_kwargs = {
            'region_1': {'write_only': True},
            'region_2': {'write_only': True},
            'region_3': {'write_only': True},
            'last_login': {'read_only': True},
            'creator_detail_on_delete': {'read_only': True},
        }


class UserRetrieveUpdateSerializer(BaseUserRetrieveUpdateSerializer):
    position = serializers.CharField(source='get_role_display', read_only=True)
    creator = serializers.URLField(source='get_creator_url', read_only=True)

    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['creator'] = self.context['request'].build_absolute_uri('/') + req['creator']
        return req


class BaseUserListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedRelatedField(view_name='user-detail', source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'phone_number', 'first_name', 'last_name',
            'is_active', 'is_deleted', 'detail'
        ]


class DeletedUserDataListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedRelatedField(view_name='deleted-user-detail', source='id', read_only=True)
    position = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = UserDetailOnDelete
        fields = ['id', 'first_name', 'last_name', 'detail', 'position']


class DeletedUserDataRetrieveSerializer(serializers.ModelSerializer):
    position = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = UserDetailOnDelete
        exclude = ['role']
