from django.contrib import admin

from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'price', 'delivery_time_in_hour',
        'creator', 'creator_detail_on_delete', 'image', 'file'
    ]
    list_display_links = ['title']
