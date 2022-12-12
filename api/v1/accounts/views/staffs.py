from rest_framework import (
    mixins,
    generics,
    exceptions,
    response,
    status
)
from rest_framework.permissions import IsAuthenticated

from api.v1.accounts.exceptions import MultiValueError
from api.v1.accounts.models import CustomUser
from api.v1.accounts.permissions import IsActive
from api.v1.accounts.serializers.staffs import StaffListSerializer
from api.v1.accounts.permissions import IsStaff
from api.v1.accounts.services import get_queryset_by_permission


class StaffListAPIView(mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = CustomUser.objects.filter(is_staff=True)
    serializer_class = StaffListSerializer
    permission_classes = [IsAuthenticated, IsActive, IsStaff]
    filterset_fields = ['role', 'is_active', 'is_deleted']
    search_fields = ['phone_number', 'email', 'first_name', 'last_name']
    ordering = '-date_joined'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            raise exceptions.ValidationError('a list type was expected')
        if len(data) > 100:
            raise MultiValueError('You can remove 100 objects in one try.')
        if not all(isinstance(i, int) for i in data):
            raise exceptions.ValidationError('"id" is not of type int')

        # users = self.get_queryset().filter(pk__in=data).exclude(pk=self.request.user.id)
        # if not self.request.user.has_perm('delete_' + str()):
        #     raise exceptions.PermissionDenied()
        # users.update(
        #     is_active=False, is_deleted=True
        # )
        return response.Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        return get_queryset_by_permission(self)

