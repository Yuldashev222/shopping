from django.db import models

from api.v1.accounts.models import Client


class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
