from django.contrib import admin

from .models import Client, Director, Manager, Vendor, Developer

admin.site.register([Client, Director, Manager, Vendor, Developer])
