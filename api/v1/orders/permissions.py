from rest_framework import permissions

from api.v1.accounts.enums import CustomUserRole


class IsOwnerOrderClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.order.client.id == request.user.id:
            return True
        return False
