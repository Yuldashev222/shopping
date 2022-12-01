from rest_framework import permissions

from api.v1.accounts.enums import CustomUserRole


class IsOwnerClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.client.id == request.user.id:
            return True
        return False


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role != CustomUserRole.client.name:
            return True
        return False


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == CustomUserRole.client.name:
            return True
        return False


class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == CustomUserRole.director.name:
            return True
        return False
