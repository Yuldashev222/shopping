from phonenumber_field import modelfields
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.html import mark_safe
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
from .services import upload_location_user_photo
from .validators import validate_size_user_photo, active_and_not_deleted_user
from .enums import CustomUserRole
from api.v1.general.enums import Regions


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = modelfields.PhoneNumberField(_("Phone number"), unique=True)
    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(_("First name"), max_length=30)
    last_name = models.CharField(_("Last name"), max_length=50)
    role = models.CharField(_("User Role"), max_length=9, choices=CustomUserRole.choices())

    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True)

    # connections
    creator = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        validators=[active_and_not_deleted_user]
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
    is_deleted = models.BooleanField(_("deleted"), default=False)

    # second fields
    desc = models.CharField(_('Description'), blank=True, max_length=500)
    second_phone_number = modelfields.PhoneNumberField(_("Second phone number"), blank=True, null=True)
    photo = models.ImageField(
        verbose_name=_('User Photo'), blank=True,
        default='avatar.png',
        upload_to=upload_location_user_photo,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'svg']),
            validate_size_user_photo
        ]
    )

    # address 1
    region_1 = models.CharField(max_length=100, choices=Regions.choices())
    district_1 = models.CharField(max_length=100, blank=True)
    street_1 = models.CharField(max_length=100, blank=True)

    # address 2
    region_2 = models.CharField(max_length=100, choices=Regions.choices(), blank=True)
    district_2 = models.CharField(max_length=100, blank=True)
    street_2 = models.CharField(max_length=100, blank=True)

    # address 3
    region_3 = models.CharField(max_length=100, choices=Regions.choices(), blank=True)
    district_3 = models.CharField(max_length=100, blank=True)
    street_3 = models.CharField(max_length=100, blank=True)

    # card 1

    def __str__(self):
        return f'{self.role}: {self.phone_number}'

    class Meta:
        db_table = 'user'
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('-date_joined', 'role')

    def get_username(self):
        return str(getattr(self, self.USERNAME_FIELD))

    def get_creator_url(self):
        if self.creator:
            return reverse('user-detail', kwargs={'pk': self.creator.id})
        return reverse('deleted-user-detail', kwargs={'pk': self.creator_detail_on_delete.id})

    def active_object(self):
        return self.is_active and not self.is_deleted

    def clean(self):
        errors = dict()

        if self.role == CustomUserRole.director.name and Director.objects.exists():
            raise ValidationError('director must be unique')

        if self.creator and self.creator_detail_on_delete:
            raise ValidationError(
                {'creator_detail_on_delete': 'this field is automatically filled when the "creator" field is deleted'}
            )

        if self.role not in [CustomUserRole.client.name, CustomUserRole.developer.name] and not self.creator:
            raise ValidationError({'creator': 'This field is required'})

        elif self.role == CustomUserRole.director.name and self.creator.role != CustomUserRole.developer.name:
            raise ValidationError({'creator': 'only the developer can add director!'})

        elif self.role == CustomUserRole.manager.name and self.creator.role not in [
            CustomUserRole.director.name, CustomUserRole.developer.name]:
            raise ValidationError({'creator': 'only the director can add managers!'})

        elif self.role == CustomUserRole.vendor.name and self.creator.role not in [
            CustomUserRole.director.name, CustomUserRole.developer.name, CustomUserRole.manager.name]:
            raise ValidationError({'creator': 'only the director or manager can add vendors!'})

        if self.phone_number == self.second_phone_number:
            errors['phone_numbers'] = ['first and second phone numbers already exists.']

        if errors:
            raise ValidationError(errors)

    @property
    def photo_preview(self):
        return mark_safe(f'<img src="{self.photo.url}" width="150" height="150" />')

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if self.role != CustomUserRole.client.name:
            self.is_staff = True
        else:
            self.is_staff = False
        if self.is_deleted:
            self.is_active = False
        super().save(*args, **kwargs)

    def email_user(self, subject, message, from_email=settings.EMAIL_HOST_USER, **kwargs):
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

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        if self.role == CustomUserRole.client.name:
            self.is_staff = False
        else:
            self.is_staff = True
        super().save(*args, **kwargs)

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
        self.role = CustomUserRole.client.name
        super().save(*args, **kwargs)


class Director(CustomUser):
    objects = DirectorManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        self.role = CustomUserRole.director.name
        super().save(*args, **kwargs)


class Manager(CustomUser):
    objects = ManagerManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        self.role = CustomUserRole.manager.name
        super().save(*args, **kwargs)


class Vendor(CustomUser):
    objects = VendorManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        self.role = CustomUserRole.vendor.name
        super().save(*args, **kwargs)


class Developer(CustomUser):
    objects = DeveloperManager()

    class Meta:
        proxy = True
        ordering = ('date_joined',)

    def save(self, *args, **kwargs):
        self.role = CustomUserRole.developer.name
        super().save(*args, **kwargs)
