from rest_framework import permissions

from api.v1.accounts.enums import CustomUserRole


class IsOwnerClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.client.id == request.user.id:
            return True
        return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.id == request.user.id)


class IsNotOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.id != request.user.id)


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.active_object()


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


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


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == CustomUserRole.manager.name:
            return True
        return False


class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == CustomUserRole.vendor.name:
            return True
        return False


class IsDeveloper(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == CustomUserRole.developer.name:
            return True
        return False
