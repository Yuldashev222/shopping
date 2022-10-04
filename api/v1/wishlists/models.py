from django.db import models

from api.v1.accounts.models import Client
from api.v1.products.models import AddToProduct


class Wishlist(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)


class AddProductToWishlist(models.Model):
    product = models.ForeignKey(AddToProduct, on_delete=models.PROTECT)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=1)
