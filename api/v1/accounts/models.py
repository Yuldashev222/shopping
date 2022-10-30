from phonenumber_field import modelfields
from django.db import models
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .services import upload_location_profile_picture
from .validators import validate_size_profile_picture
from .managers import (
    CustomUserManager,
    ClientManager,
    DirectorManager,
    ManagerManager,
    DeveloperManager,
    VendorManager,
    StaffManager,
    LeaderManager,
)
from .enums import CustomUserRole


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = modelfields.PhoneNumberField(_("Phone number"), unique=True)
    second_phone_number = modelfields.PhoneNumberField(_("Second phone number"), blank=True)
    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(_("First name"), max_length=30)
    last_name = models.CharField(_("Last name"), max_length=50)
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, editable=False)
    role = models.CharField(_("User Role"), max_length=9, choices=CustomUserRole.choices())
    creator = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)  # last

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_deleted = models.BooleanField(_("Is deleted"), default=False)
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
        ],
        null=True
    )

    # address 1
    country_1 = models.CharField(max_length=15, blank=True)
    region_1 = models.CharField(max_length=100, blank=True)
    district_1 = models.CharField(max_length=100, blank=True)
    street_1 = models.CharField(max_length=100, blank=True)

    # address 2
    country_2 = models.CharField(max_length=15, blank=True)
    region_2 = models.CharField(max_length=100, blank=True)
    district_2 = models.CharField(max_length=100, blank=True)
    street_2 = models.CharField(max_length=100, blank=True)

    # address 3
    country_3 = models.CharField(max_length=15, blank=True)
    region_3 = models.CharField(max_length=100, blank=True)
    district_3 = models.CharField(max_length=100, blank=True)
    street_3 = models.CharField(max_length=100, blank=True)

    # card 1

    def __str__(self):
        return self.get_full_name()

    def active_object(self):
        return self.is_active and not self.is_deleted

    def clean(self):
        errors = dict()

        if self.phone_number == self.second_phone_number:
            errors['phone_numbers'] = ['first and second phone numbers already exists.']

        if errors:
            raise ValidationError(errors)

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
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('date_joined', 'role')
        constraints = (
            models.UniqueConstraint(
                name='unique_director_role',
                fields=['role'],
                condition=models.Q(role=CustomUserRole.director.value)
            ),
        )


class Client(CustomUser):
    objects = ClientManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)


class Director(CustomUser):
    objects = DirectorManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)


class Manager(CustomUser):
    objects = ManagerManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)


class Developer(CustomUser):
    objects = DeveloperManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)


class Vendor(CustomUser):
    objects = VendorManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)


class Staff(CustomUser):
    objects = StaffManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)


class Leader(CustomUser):
    objects = LeaderManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)
