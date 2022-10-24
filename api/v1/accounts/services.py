from rest_framework_simplejwt.tokens import RefreshToken, Token


def upload_location_profile_picture(instance, picture):
    """
    Rasmga joylashgan address | format: (media)/accounts/role/pictures/user/picture
    """
    return f'accounts/{instance.role}/pictures/{instance.get_full_name()}/{picture}'


def get_tokens_user(user):
    refresh = RefreshToken.for_user(user)
    return refresh
