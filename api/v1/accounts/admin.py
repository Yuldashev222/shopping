from django.contrib import admin
from django.contrib.auth.models import ContentType

from .models import (
    UserDetailOnDelete,
    Client,
    Director,
    Manager,
    Vendor,
    Developer
)


class BaseUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'email', 'first_name', 'last_name']
    list_display_links = ['phone_number']


class UserDetailOnDeleteAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display
    list_display.insert(1, 'role')
    list_filter = ['role']


admin.site.register(Developer, BaseUserAdmin)
admin.site.register(Client, BaseUserAdmin)
admin.site.register(Director, BaseUserAdmin)
admin.site.register(Manager, BaseUserAdmin)
admin.site.register(Vendor, BaseUserAdmin)
admin.site.register(UserDetailOnDelete, UserDetailOnDeleteAdmin)

