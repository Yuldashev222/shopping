from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.core.validators import ValidationError

@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Enter a valid phone_number. This value may contain only letters, "
        "numbers, and + a plus."
    )
    flags = 0


def validate_phone_number(phone_number: str):
    if len(phone_number) != 13 or len(phone_number) != 9 or len(phone_number) != 12:
        raise


def validate_size_profile_picture(picture):
    """
    Rasm hajmini tekshirish
    """

    size_limit = 5
    if picture.size > size_limit * 1024 * 1024:
        raise ValidationError(f'maximum picture size: {size_limit}mb')
