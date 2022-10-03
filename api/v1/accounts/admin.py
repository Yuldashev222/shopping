from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Vendor, Client, Manager

admin.site.register([Vendor, Client, Manager])


@admin.register(auth.get_user_model())
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "phone_number", "date_joined", "last_login", "is_admin", "is_staff")
    search_fields = ("email", "phone_number")
    readonly_fields = ("id", "date_joined", "last_login")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('phone_number',)

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "email", "password1", "password2"),
            },
        ),
    )
