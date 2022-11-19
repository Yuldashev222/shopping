from rest_framework import permissions

from api.v1.accounts.enums import CustomUserRole


class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role != CustomUserRole.client.value or request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role != CustomUserRole.client.value or request.method in permissions.SAFE_METHODS:
            return True
        return False
