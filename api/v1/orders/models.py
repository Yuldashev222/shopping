from django.db import models
from django.utils.translation import gettext_lazy as _

from api.v1.accounts.models import Client
from api.v1.carts.models import Cart
from .enums import OrderStatuses


class Order(models.Model):
    order_id = models.IntegerField(verbose_name=_('ORDER ID'), )
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    status = models.CharField(max_length=10, choices=OrderStatuses.choices())
