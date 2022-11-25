from rest_framework import permissions

from api.v1.accounts.enums import CustomUserRole


class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == CustomUserRole.director.name:
            return True
        return False


class IsLeader(permissions.BasePermission):
    def has_permission(self, request, view):
        leaders = [CustomUserRole.director.name, CustomUserRole.manager.name]
        if request.user.role in leaders:
            return True
        return False
