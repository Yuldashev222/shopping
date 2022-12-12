from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status

from api.v1.accounts.enums import CustomUserRole
from api.v1.accounts.models import CustomUser
from api.v1.accounts.permissions import IsActive, IsStaff, IsNotOwner, IsOwner
from api.v1.accounts.serializers.all_users import UserRetrieveUpdateSerializer
from api.v1.accounts.serializers.clients import OwnerClientRetrieveUpdateSerializer
from api.v1.accounts.serializers.staffs import OwnerStaffRetrieveUpdateSerializer
from api.v1.accounts.services import get_queryset_by_permission


class StaffRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsActive, IsStaff, IsNotOwner]  # last
    serializer_class = UserRetrieveUpdateSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        request_user_role = self.request.user.role
        if (
                request_user_role == CustomUserRole.vendor.name and obj.role != CustomUserRole.client.name
                or
                request_user_role == CustomUserRole.manager.name and
                obj.role in [CustomUserRole.developer.name, CustomUserRole.director.name, CustomUserRole.manager.name]
                or
                request_user_role == CustomUserRole.director.name and
                obj.role in [CustomUserRole.developer.name, CustomUserRole.director.name]
                or
                request_user_role == CustomUserRole.developer.name == obj.role
        ):
            self.serializer_class = OwnerStaffRetrieveUpdateSerializer

        return obj

    def get_queryset(self):
        return get_queryset_by_permission(self)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request_role = self.request.user.role

        if (
                instance.role == CustomUserRole.developer.name and
                request_role != CustomUserRole.developer.name
                or
                instance.role == CustomUserRole.director.name and
                request_role not in [CustomUserRole.developer.name, CustomUserRole.director.name]
                or
                (instance.role == CustomUserRole.manager.name or instance.role == CustomUserRole.vendor.name) and
                request_role not in
                [CustomUserRole.developer.name, CustomUserRole.director.name, CustomUserRole.manager.name]

        ):
            raise PermissionDenied()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user.has_perm('delete_' + str(instance.role)):
            raise PermissionDenied()

        instance.is_deleted = True
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OwnerUserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsActive, IsOwner, DjangoModelPermissions]
    queryset = CustomUser.objects.filter(is_active=True, is_deleted=False)

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.user.role == CustomUserRole.client.name:
            return OwnerClientRetrieveUpdateSerializer  # last
        return OwnerStaffRetrieveUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_staff:
            raise PermissionDenied()

        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
