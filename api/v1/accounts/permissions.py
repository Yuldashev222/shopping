from rest_framework import permissions

from api.v1.accounts.enums import CustomUserRole


class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == CustomUserRole.director.value:
            return True
        return False


class IsLeader(permissions.BasePermission):
    def has_permission(self, request, view):
        leaders = [CustomUserRole.director.value, CustomUserRole.manager.value]
        if request.user.role in leaders:
            return True
        return False
