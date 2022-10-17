from django.contrib.auth.base_user import BaseUserManager
from django.apps import apps
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib import auth

from .enums import CustomUserRole


class CustomUserManager(BaseUserManager):
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

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label,
            self.model._meta.object_name
        )
        user = self.model(
            phone_number=phone_number,
            role=role,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields)

        user.password = make_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, phone_number, role, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            phone_number=phone_number,
            role=role,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields
        )

    def create_superuser(self, phone_number, first_name, last_name, email=None, password=None, **extra_fields):
        role = CustomUserRole.developer.value
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            phone_number=phone_number,
            role=role,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields
        )

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class ClientManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.client.value)


class DirectorManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.director.value)


class ManagerManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.manager.value)


class DeveloperManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.developer.value)


class VendorManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUserRole.vendor.value)


class StaffManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role__in=(
            CustomUserRole.director.value,
            CustomUserRole.manager.value,
            CustomUserRole.vendor.value
        ))


class LeaderManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role__in=(
            CustomUserRole.director.value,
            CustomUserRole.manager.value,
        ))
