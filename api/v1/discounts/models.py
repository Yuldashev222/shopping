from django.db import models
from django.utils.timezone import now as datetime_now

from api.v1.accounts.models import Manager
from api.v1.products.models import AddToProduct
from . import enums


class Discount(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=enums.DiscountType.choices())
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    per_client_limit = models.PositiveSmallIntegerField(blank=True, null=True)

    # discount types
    # ------------------
    # 1 - price or percent
    price_or_percent = models.PositiveIntegerField(blank=True, null=True)
    is_percent = models.BooleanField(default=True)

    # 2 - min sum max sum
    minimum_purchase = models.IntegerField(blank=True, null=True)

    # 3 - Buy n items and get the (n + 1)th free!
    free_quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    quantity_to_free_quantity = models.PositiveSmallIntegerField(blank=True, null=True)

    # 4 - free delivery service
    free_delivery = models.BooleanField(default=False)
    # --------------------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)


class ProductDiscount(models.Model):
    product = models.ForeignKey(AddToProduct, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, models.PROTECT)
    creator = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
