from django.contrib import admin

from .models import Wishlist, AddProductToWishlist

admin.site.register([Wishlist, AddProductToWishlist])
