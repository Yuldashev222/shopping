from rest_framework import (
    response,
    status,
    generics,
    exceptions,
    mixins,
    permissions,
)

from api.v1.accounts.enums import CustomUserRole
from api.v1.accounts.exceptions import MultiValueError
from api.v1.accounts.permissions import IsActive, IsStaff
from api.v1.accounts.models import CustomUser
from api.v1.accounts.serializers.clients import ClientListSerializer


class ClientListAPIView(mixins.ListModelMixin,
                        generics.GenericAPIView):

    queryset = CustomUser.objects.filter(role=CustomUserRole.client.name)
    serializer_class = ClientListSerializer
    permission_classes = [permissions.IsAuthenticated, IsActive, IsStaff, permissions.DjangoModelPermissions]
    filterset_fields = ['is_active', 'is_deleted', 'region_1']
    search_fields = ['phone_number', 'email', 'first_name', 'last_name']
    ordering = '-date_joined'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            raise exceptions.ValidationError('a list type was expected')
        elif len(data) > 100:
            raise MultiValueError('You can remove 100 objects in one try.')
        elif not all(isinstance(i, int) for i in data):
            raise exceptions.ValidationError('"id" is not of type int')
        self.queryset.filter(pk__in=data).update(is_active=False, is_deleted=True)
        return response.Response(status=status.HTTP_200_OK)

