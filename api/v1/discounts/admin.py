from django.contrib import admin

from .models import Discount, AddDiscountToProduct

admin.site.register([Discount, AddDiscountToProduct])