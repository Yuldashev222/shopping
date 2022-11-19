from django.db import models

from api.v1.accounts.enums import CustomUserRole
from api.v1.accounts.models import Client
from api.v1.products.models import Product


class Wishlist(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True, 'is_deleted': False, 'role': CustomUserRole.client.name}
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
