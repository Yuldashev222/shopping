from django.db import models

from api.v1.accounts.models import Client
from api.v1.products.models import ProductItem


class Wishlist(models.Model):
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.client}: {self.product}'

    class Meta:
        unique_together = ['product', 'client']
