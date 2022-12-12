from django.db.models import Q

from .enums import CustomUserRole
from . import models


def upload_location_user_photo(instance, photo):
    """
    Rasmga joylashgan address | format: (media)/accounts/role/photos/user/photo
    """
    return f'accounts/{instance.role}/{instance.get_full_name()}/photos/{photo}'


def get_queryset_by_permission(self):
    request_role = self.request.user.role
    if request_role == CustomUserRole.vendor.name:
        queryset = models.CustomUser.objects.exclude(
            Q(role=CustomUserRole.developer.name) |
            (Q(role=CustomUserRole.manager.name) & (Q(is_active=False) | Q(is_deleted=True))) |
            (Q(role=CustomUserRole.vendor.name) & (Q(is_active=False) | Q(is_deleted=True))) |
            (Q(role=CustomUserRole.director.name) & (Q(is_active=False) | Q(is_deleted=True)))
        )

    elif request_role == CustomUserRole.manager.name:
        queryset = models.CustomUser.objects.exclude(
            Q(role=CustomUserRole.developer.name) |
            (Q(role=CustomUserRole.manager.name) & (Q(is_active=False) | Q(is_deleted=True))) |
            (Q(role=CustomUserRole.director.name) & (Q(is_active=False) | Q(is_deleted=True)))
        )

    elif request_role == CustomUserRole.director.name:
        queryset = models.CustomUser.objects.exclude(role=CustomUserRole.developer.name)

    else:
        queryset = models.CustomUser.objects.all()

    return queryset
