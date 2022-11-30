from django.contrib import admin

from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_item', 'client', 'date_added']
    list_display_links = ['product_item']
    list_filter = ['date_added']
