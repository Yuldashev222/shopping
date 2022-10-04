from django.db import models

from api.v1.accounts.models import Client
from api.v1.products.models import AddToProduct


class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)


class AddProductToCart(models.Model):
    product = models.ForeignKey(AddToProduct, on_delete=models.PROTECT)
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    count = models.PositiveSmallIntegerField(default=1)

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
