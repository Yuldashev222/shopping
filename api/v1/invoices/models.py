from django.db import models

from api.v1.orders.models import Order
from api.v1.general.models import ShopAbout


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    shop = models.ForeignKey(ShopAbout, on_delete=models.SET_NULL, null=True)
    contract_file = models.FileField(upload_to='Invoices/Files/contracts/')

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
