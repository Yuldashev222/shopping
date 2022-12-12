from django.core.validators import ValidationError
from django.contrib.auth import get_user_model

from .enums import CustomUserRole


def validate_size_user_photo(picture):
    """
    Rasm hajmini tekshirish
    """
    size_limit = 10
    if picture.size > size_limit * 1024 * 1024:
        raise ValidationError(f'maximum photo size: {size_limit}mb')


def is_manager(user_id):
    user = get_user_model().objects.get(pk=user_id)
    if user.role != CustomUserRole.manager.name:
        raise ValidationError('user role must be manager')


def is_staff(user_id):
    user = get_user_model().objects.get(pk=user_id)
    if not user.is_staff:
        raise ValidationError('user must be an staff')


def is_client(user_id):
    user = get_user_model().objects.get(pk=user_id)
    if user.role != CustomUserRole.client.name:
        raise ValidationError('user must be an client')


def is_vendor(user_id):
    user = get_user_model().objects.get(pk=user_id)
    if user.role != CustomUserRole.vendor.name:
        raise ValidationError('user must be an vendor')


def is_director(user_id):
    user = get_user_model().objects.get(pk=user_id)
    if user.role != CustomUserRole.director.name:
        raise ValidationError('user must be an director')


def is_manager_or_director(user_id):
    user_role = get_user_model().objects.get(pk=user_id).role
    if user_role not in [CustomUserRole.director.name, CustomUserRole.manager.name, CustomUserRole.developer.name]:
        raise ValidationError('user must be an director or manager')


def active_and_not_deleted_user(user_id):
    user = get_user_model().objects.get(pk=user_id)
    if not user.active_object():
        raise ValidationError('object is not active')
