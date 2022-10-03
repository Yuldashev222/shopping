from django.contrib.auth.models import BaseUserManager
from django.db.models.manager import Manager

from .enums import CustomUserRoles


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, phone_number, last_name, role, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if not first_name:
            raise ValueError('Users must have an first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not role:
            raise ValueError('Users must have a role')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, phone_number, last_name, role, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class VendorsManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRoles.vendor.value)


class ClientsManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRoles.client.value)


class ManagersManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRoles.manager.value)
