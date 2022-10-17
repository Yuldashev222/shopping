from phonenumber_field import modelfields
from django.db import models
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, User, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .services import upload_location_profile_picture
from .validators import validate_size_profile_picture
from .managers import CustomUserManager
from .enums import CustomUserRole


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = modelfields.PhoneNumberField(_("phone number"), unique=True)
    email = models.EmailField(_("email address"), blank=True)
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=50)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True, editable=False)
    role = models.CharField(_("User Role"), max_length=9, choices=CustomUserRole.choices())
    creator = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['role', 'first_name', 'last_name']

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_superuser = models.BooleanField(_("superuser status"), default=False)

    # second fields
    desc = models.CharField(_('Description'), blank=True, max_length=500)
    profile_picture = models.ImageField(
        verbose_name=_('Profile picture'),
        upload_to=upload_location_profile_picture,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'svg']),
            validate_size_profile_picture
        ]
    ),

    # country_1 = models.CharField(
    #     max_length=15,
    #     blank=True
    # )
    # region_1 = models.CharField(max_length=100, blank=True)
    # district_1 = models.CharField(max_length=100, blank=True)
    # street_1 = models.CharField(max_length=100, blank=True)
    #
    # # constant address
    # region_2 = models.CharField(
    #     max_length=15,
    #     blank=True,
    #     null=True,
    #     help_text='your current state of residence'
    # )
    # city_2 = models.CharField(
    #     max_length=100,
    #     blank=True,
    #     null=True,
    #     help_text='your current city of residence'
    # )
    # street_2 = models.CharField(
    #     max_length=100,
    #     blank=True,
    #     null=True,
    #     help_text='your current residential address'
    # )

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
