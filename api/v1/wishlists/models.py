from django.db import models

from api.v1.accounts.models import Client


class Wishlist(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
