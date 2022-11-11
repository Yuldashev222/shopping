from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from api.v1.accounts.models import Client
from api.v1.products.models import ProductItem
from api.v1.delivery.models import Delivery
from .services import upload_location_order_contract_file


class Order(models.Model):
    order_id = models.PositiveSmallIntegerField(verbose_name=_('ORDER ID'))
    contract_file = models.FileField(upload_to=upload_location_order_contract_file, blank=True, null=True)

    # connections
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_deleted = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order_id}. Client: {self.client}'

    def active_object(self):
        return not self.is_deleted


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()

    # connections
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        limit_choices_to={'is_deleted': False, 'is_confirmed': False}
    )
    product = models.ForeignKey(
        ProductItem,
        on_delete=models.PROTECT,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    # -----------

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'order'],
                name='product_order_unique'
            )
        ]

    def __str__(self):
        return f'{self.order.client}: {self.product.product.name}'

    def clean(self):

        if self.quantity > self.product.count_in_stock:
            raise ValidationError({'quantity': 'There are not enough products in the warehouse'})

    def active_object(self):
        return self.is_active and not self.is_deleted
