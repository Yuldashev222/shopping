from django.db import models
from django.utils.translation import gettext_lazy as _

from api.v1.accounts.models import Client
from api.v1.products.models import ProductItem
from .services import upload_location_order_contract_file


class Order(models.Model):
    order_id = models.PositiveSmallIntegerField(verbose_name=_('ORDER ID'))
    contract_file = models.FileField(upload_to=upload_location_order_contract_file, blank=True, null=True)

    # connections
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order_id}. Client: {self.client}'


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField(default=1)

    # connections
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(ProductItem, on_delete=models.PROTECT)
    # -----------

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}: {self.quantity}'
