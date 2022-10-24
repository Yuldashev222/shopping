from rest_framework import permissions

from api.v1.accounts.enums import CustomUserRole


class IsStaffOrReadOnly(permissions.BasePermission):
    staff_roles = (CustomUserRole.director.value, CustomUserRole.manager.value, CustomUserRole.vendor.value)

    def has_permission(self, request, view):
        if request.user.role in self.staff_roles or request.method in permissions.SAFE_METHODS:
            return True
        return False
