from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password

from .enums import CustomUserRole


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, role, first_name, last_name, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")
        if not role:
            raise ValueError("The given role must be set")
        if not first_name:
            raise ValueError("The given first name must be set")
        if not last_name:
            raise ValueError("The given last name must be set")
        email = self.normalize_email(email)

        user = self.model(
            phone_number=phone_number,
            role=role,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(**extra_fields)

    def create_superuser(self, **extra_fields):
        role = CustomUserRole.developer.name
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(role=role, **extra_fields)


class ClientManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.client.name)


class DirectorManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.director.name)

    def _create_user(self, **extra_fields):
        role = CustomUserRole.director.name
        super()._create_user(role=role, **extra_fields)

    def create(self, role=None, *args, **kwargs):
        role = CustomUserRole.director.name
        super().create(role=role, *args, **kwargs)


class ManagerManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.manager.name)


class VendorManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.vendor.name)


class DeveloperManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.developer.name)
