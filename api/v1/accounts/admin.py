from django.contrib.auth.models import Group
from django.contrib import admin

from .models import Client, Director, Manager, Vendor

admin.site.register([Client, Director, Manager, Vendor])
# admin.site.unregister(Group)
