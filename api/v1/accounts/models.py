from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field import modelfields
from django.contrib.auth import get_user_model

from . import managers, enums, services


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    father_name = models.CharField(_("father name"), max_length=70, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    phone_number = modelfields.PhoneNumberField(unique=True)
    role = models.CharField(max_length=10, choices=enums.CustomUserRoles.choices())

    desc = models.CharField(max_length=1000, blank=True, null=True)
    second_phone_number = modelfields.PhoneNumberField(blank=True, null=True)

    objects = managers.CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'role']

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True,
                                       editable=False)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True,
                                      editable=False)

    profile_image = models.ImageField(
        upload_to=services.upload_location_profile_image,
        validators=[
            FileExtensionValidator(allowed_extensions=('jpg', 'png', 'jpeg', 'svg')),
            services.validate_size_image
        ],
        null=True,
        blank=True,
        # default profile image ...
    )

    home1_address_country = models.CharField(max_length=100, help_text='country in home',
                                             blank=True, null=True)
    home1_address_region = models.CharField(max_length=100, help_text='region in home',
                                            blank=True, null=True)
    home1_address_street = models.CharField(max_length=100, help_text='street in home',
                                            blank=True, null=True)
    home2_address_country = models.CharField(max_length=100, help_text='country in second home',
                                             blank=True, null=True)
    home2_address_region = models.CharField(max_length=100, help_text='region in second home',
                                            blank=True, null=True)
    home2_address_street = models.CharField(max_length=100, help_text='street in second home',
                                            blank=True, null=True)
    office_address_country = models.CharField(max_length=100, help_text='address country in office',
                                              blank=True, null=True)
    office_address_region = models.CharField(max_length=100, help_text='address region in office',
                                             blank=True, null=True)
    office_address_street = models.CharField(max_length=100, help_text='address street in office',
                                             blank=True, null=True)

    def __str__(self):
        if self.father_name:
            return self.first_name + '-' + self.last_name + '-' + self.father_name
        return self.first_name + '-' + self.last_name

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class Client(get_user_model()):
    objects = managers.ClientsManager()

    class Meta:
        proxy = True


class Manager(get_user_model()):
    objects = managers.ManagersManager()

    class Meta:
        proxy = True


class Vendor(get_user_model()):
    objects = managers.VendorsManager()

    class Meta:
        proxy = True
