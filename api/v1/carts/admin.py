from django.contrib import admin

from .models import Cart, AddProductToCart

admin.site.register([Cart, AddProductToCart])
