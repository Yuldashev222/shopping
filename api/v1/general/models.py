from django.db import models

from api.v1.accounts.models import Manager


class ShopAbout(models.Model):
    name = models.CharField(max_length=255, null=True)
    creator = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
