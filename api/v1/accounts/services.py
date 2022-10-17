from django.core.exceptions import ValidationError


def upload_location_profile_picture(instance, picture):
    """
    Faylga joylashgan address | format: (media)/accounts/role/pictures/user/picture
    """
    return f'accounts/{instance.role}/pictures/{instance.get_full_name()}/{picture}'
