from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.accounts.models import UserDetailOnDelete
from api.v1.products.models import ProductItem
from api.v1.products.validators import active_and_not_deleted_product
from api.v1.accounts.validators import is_client, active_and_not_deleted_user
from api.v1.orders.validators import active_and_not_deleted_order

from .services import upload_location_order_contract_file
from .validators import not_confirmed


class Order(models.Model):
    order_id = models.PositiveSmallIntegerField(
        unique=True, validators=[MinValueValidator(1)], verbose_name=_('ORDER ID')
    )
    desc = models.TextField(max_length=1000, blank=True)
    contract_file = models.FileField(upload_to=upload_location_order_contract_file, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)  # last

    # connections
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_client]
    ),
    client_detail_on_delete = models.ForeignKey(
        UserDetailOnDelete, on_delete=models.PROTECT,
        blank=True, null=True
    )
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order_id}. Client: {self.client}'

    class Meta:
        db_table = 'order'

    def clean(self):
        if self.client and self.client_detail_on_delete:
            raise ValidationError({'client_detail_on_delete': 'cannot be this field when the "client" field exists'})

    def active_object(self):
        return self.is_active and not self.is_deleted


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=1)

    # connections
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items',
        validators=[active_and_not_deleted_order, not_confirmed],
    )
    product_item = models.ForeignKey(
        ProductItem, on_delete=models.PROTECT,
        validators=[active_and_not_deleted_product],
    )
    # -----------

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_item'
        constraints = [
            models.UniqueConstraint(
                fields=['product_item', 'order'],
                name='product_order_unique'
            )
        ]

    def __str__(self):
        return f'{self.order.client}: {self.product_item.product.name}'

    def clean(self):
        if self.quantity > self.product_item.count_in_stock:
            raise ValidationError({'quantity': 'There are not enough products in the warehouse'})

    def active_object(self):
        return self.is_active and not self.is_deleted
