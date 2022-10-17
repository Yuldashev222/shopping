from django.core.validators import ValidationError


def validate_size_profile_picture(picture):
    """
    Rasm hajmini tekshirish
    """
    size_limit = 5
    if picture.size > size_limit * 1024 * 1024:
        raise ValidationError(f'maximum picture size: {size_limit}mb')
