from django.db import models


class ShopAbout(models.Model):
    name = models.CharField(max_length=255, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False, null=True)
