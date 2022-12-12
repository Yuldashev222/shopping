from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from api.v1.accounts.models import UserDetailOnDelete
from api.v1.accounts.serializers.all_users import (
    DeletedUserDataListSerializer,
    DeletedUserDataRetrieveSerializer
)
from api.v1.accounts.permissions import IsActive
from api.v1.accounts.exceptions import MultiValueError


class DeletedUserDataAPIViewSet(RetrieveModelMixin,
                                ListModelMixin,
                                DestroyModelMixin,
                                GenericViewSet):
    queryset = UserDetailOnDelete.objects.all()
    permission_classes = [IsAuthenticated, IsActive, DjangoModelPermissions]
    filterset_fields = ['role', 'date_joined', 'date_deleted']
    search_fields = ['email', 'phone_number', 'first_name', 'last_name']
    ordering = 'date_deleted'

    def get_serializer_class(self):
        if self.action == 'list':
            return DeletedUserDataListSerializer
        return DeletedUserDataRetrieveSerializer

    def delete(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.destroy(request, *args, **kwargs)

        data = request.data
        if not isinstance(data, list):
            raise ValidationError('a list type was expected')
        elif len(data) > 100:
            raise MultiValueError('You can remove 100 objects in one try.')
        elif not all(isinstance(i, int) for i in data):
            raise ValidationError('"id" is not of type int')
        UserDetailOnDelete.objects.filter(pk__in=data).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
