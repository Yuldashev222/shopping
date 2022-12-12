from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    UserDetailOnDelete,
    Developer,
    CustomUser
)


@admin.register(CustomUser)
class BaseUserAdmin(admin.ModelAdmin):

    list_display = ['id', 'role', 'phone_number', 'email', 'first_name', 'last_name', 'date_joined']
    list_filter = ['role', 'region_1', 'is_active', 'is_deleted']
    list_display_links = ['phone_number']
    exclude = ['groups', 'is_staff']
    readonly_fields = [
        'photo_preview', 'last_login', 'role', 'date_joined',
        'date_updated'
    ]
    fields = [
        ('photo_preview', 'photo'), 'role',
        ('phone_number', 'email', 'password'),
        ('first_name', 'last_name', 'desc'),
        ('creator', 'creator_detail_on_delete', 'second_phone_number'),
        ('region_1', 'district_1', 'street_1'),
        ('region_2', 'district_2', 'street_2'),
        ('region_3', 'district_3', 'street_3'),
        ('is_active', 'is_deleted'),
        'last_login', 'date_joined', 'date_updated'
    ]

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = 'Photo'
    photo_preview.allow_tags = True

    def add_view(self, request, form_url='', extra_context=None):
        data = request.GET.copy()
        data['creator'] = request.user
        request.GET = data
        return super(BaseUserAdmin, self).add_view(request, form_url='', extra_context=extra_context)


class DeveloperAdmin(BaseUserAdmin):
    fields = [
        ('photo_preview', 'photo'),
        ('phone_number', 'email', 'password'),
        ('first_name', 'last_name', 'desc'),
        'last_login',
        'date_joined',
        'date_updated',
    ]


class UserDetailOnDeleteAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'email', 'role', 'date_deleted']
    list_display_links = ['phone_number']
    list_filter = ['role']


# admin.site.register(Developer, DeveloperAdmin)
admin.site.register(UserDetailOnDelete, UserDetailOnDeleteAdmin)
