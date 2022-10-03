from django.core.exceptions import ValidationError


def upload_location_profile_image(instance, file):
    """
    Faylga joylashgan address | format: (media)/company/avatars/section/role/first_name-last_name-father_name/
    """
    return f'{instance.role}/profile_images/{instance}/{file}'


def validate_size_image(file_in_obj):
    """
    Rasm hajmini tekshirish
    """

    size_limit = 2
    if file_in_obj.size > size_limit * 1024 * 1024:
        raise ValidationError(f'maximum file size: {size_limit}mb')
