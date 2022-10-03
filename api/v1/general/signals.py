from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from rest_framework.serializers import ValidationError

from .models import ShopAbout


@receiver(pre_save, sender=ShopAbout)
def save_shop_about(*args, **kwargs):
    print(args, kwargs)
    print()
    print()
    print()
    if ShopAbout.objects.exists():
        print(1111111111)
        ValidationError({'error': ['there should be only one object in this table!']})
