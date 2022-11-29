from django.db import models
from django.conf import settings

from api.v1.accounts.validators import is_client, active_and_not_deleted_user
from api.v1.accounts.models import Client
from api.v1.products.models import ProductItem
from api.v1.products.validators import active_and_not_deleted_product_item


class Wishlist(models.Model):
    product_item = models.ForeignKey(
        ProductItem, on_delete=models.PROTECT,
        validators=[active_and_not_deleted_product_item],
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        validators=[active_and_not_deleted_user, is_client],
    )

    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.product_item} >> {self.client}'

    class Meta:
        db_table = 'wishlist'
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'product_item'],
                name='client_product_item_unique_wishlist'
            )
        ]
