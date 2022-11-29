from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Discount


@receiver(post_save, sender=Discount)
def save_remaining_discount_quantity(instance, *args, **kwargs):
    if kwargs.get('created', False):
        instance.remaining_discount_quantity = instance.discount_quantity
