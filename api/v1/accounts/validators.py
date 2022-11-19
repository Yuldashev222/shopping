from django.core.validators import ValidationError

from .enums import CustomUserRole


def validate_size_profile_picture(picture):
    """
    Rasm hajmini tekshirish
    """
    size_limit = 10
    if picture.size[0] * picture.size[1] > size_limit * 1024 * 1024:
        raise ValidationError(f'maximum picture size: {size_limit}mb')


def leader_user(user):
    if user.role not in [CustomUserRole.manager.name, CustomUserRole.director.name]:
        raise ValidationError('user role must be director or manager')
