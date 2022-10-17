from django.db import models

from api.v1.accounts.models import Client
from api.v1.products.models import AddToProduct


class WishlistProductItem(models.Model):
    product = models.ForeignKey(AddToProduct, on_delete=models.PROTECT)
    count = models.PositiveSmallIntegerField(default=1)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
