from django.core.exceptions import ValidationError
from re import compile as re_compile
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

COLOR_HEXA_RE = re_compile("#([A-Fa-f0-9]{8}|[A-Fa-f0-9]{4})$")
validate_color_hexa = RegexValidator(
    COLOR_HEXA_RE,
    _("Enter a valid hexa color, eg. #00000000"), "invalid"
)
