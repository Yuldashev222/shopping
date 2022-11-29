from phonenumber_field import modelfields
from django.db import models
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

from .managers import (
    CustomUserManager,
    ClientManager,
    DirectorManager,
    ManagerManager,
    VendorManager,
    DeveloperManager
)
from .services import upload_location_profile_picture
from .validators import validate_size_profile_picture, is_manager_or_director, active_and_not_deleted_user
from .enums import CustomUserRole


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = modelfields.PhoneNumberField(_("Phone number"), unique=True)
    second_phone_number = modelfields.PhoneNumberField(_("Second phone number"), blank=True, null=True)
    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(_("First name"), max_length=30)
    last_name = models.CharField(_("Last name"), max_length=50)
    role = models.CharField(_("User Role"), max_length=9, choices=CustomUserRole.choices())

    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, editable=False)

    # connections
    creator = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        validators=[active_and_not_deleted_user, is_manager_or_director]
    )
    creator_detail_on_delete = models.ForeignKey(
        'UserDetailOnDelete', on_delete=models.PROTECT, blank=True, null=True
    )
    # ----------

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_deleted = models.BooleanField(_("Is deleted"), default=False)

    # second fields
    desc = models.CharField(_('Description'), blank=True, max_length=500)
    profile_picture = models.ImageField(
        verbose_name=_('Profile picture'), blank=True, null=True,
        upload_to=upload_location_profile_picture,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'svg']),
            validate_size_profile_picture
        ]
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
        return f'{self.role}: {self.phone_number}'

    class Meta:
        db_table = 'user'
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('date_joined', 'role')
        constraints = (
            models.UniqueConstraint(
                name='unique_director_role',
                fields=['role'],
                condition=models.Q(role=CustomUserRole.director.name)
            ),
        )

    def get_username(self):
        return str(getattr(self, self.USERNAME_FIELD))

    def active_object(self):
        return self.is_active and not self.is_deleted

    def clean(self):
        errors = dict()

        if self.role != CustomUserRole.client.name and not self.creator:
            raise ValidationError({'creator': 'This field is required'})

        if self.role == CustomUserRole.manager.name and self.creator.role != CustomUserRole.director.name:
            raise ValidationError({'creator': 'only the director can add managers!'})

        if self.creator and self.creator_detail_on_delete:
            raise ValidationError(
                {'creator_detail_on_delete': 'this field is automatically filled when the "creator" field is deleted'}
            )

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role != CustomUserRole.client.name:
            self.is_staff = True
        else:
            self.is_staff = False

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserDetailOnDelete(models.Model):
    phone_number = modelfields.PhoneNumberField()
    email = models.EmailField()
    role = models.CharField(max_length=9, choices=CustomUserRole.choices())
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField()
    date_deleted = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.phone_number}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == CustomUserRole.client.name:
            self.is_staff = False
        else:
            self.is_staff = True

    class Meta:
        db_table = 'user_detail_on_delete'
        verbose_name = 'Deleted User Detail'
        verbose_name_plural = 'Users detail on delete'


class Client(CustomUser):
    objects = ClientManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.role = CustomUserRole.client.name


class Director(CustomUser):
    objects = DirectorManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.role = CustomUserRole.director.name


class Manager(CustomUser):
    objects = ManagerManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.role = CustomUserRole.manager.name


class Vendor(CustomUser):
    objects = VendorManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.role = CustomUserRole.vendor.name


class Developer(CustomUser):
    objects = DeveloperManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.role = CustomUserRole.developer.name
