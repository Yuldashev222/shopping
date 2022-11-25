from django.db import models
from django.conf import settings

from api.v1.accounts.validators import is_client, active_and_not_deleted_user
from api.v1.accounts.models import Client
from api.v1.products.models import Product
from api.v1.products.validators import active_and_not_deleted_product


class Wishlist(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT,
        validators=[active_and_not_deleted_product],
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        validators=[active_and_not_deleted_user, is_client],
    )

    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.client}: {self.product}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'product'],
                name='client_product_unique_wishlist'
            )
        ]
