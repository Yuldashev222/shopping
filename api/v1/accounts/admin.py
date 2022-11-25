from django.contrib import admin
from django.contrib.auth.models import Permission, ContentType
from django.contrib.sessions.models import Session

from .models import CustomUser, UserDetailOnDelete

admin.site.register([Permission, Session])


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'phone_number', 'email', 'first_name', 'last_name']
    list_display_links = ['phone_number', 'role']
    list_filter = ['role']


@admin.register(UserDetailOnDelete)
class UserDetailOnDeleteAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'phone_number', 'email', 'first_name', 'last_name']
    list_display_links = ['phone_number', 'role']
    list_filter = ['role']
