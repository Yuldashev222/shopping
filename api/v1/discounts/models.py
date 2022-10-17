from django.db import models

from api.v1.accounts.models import Leader
from api.v1.products.models import ProductItem
from . import enums


class Discount(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=enums.DiscountType.choices())
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    all_quantity = models.PositiveIntegerField(blank=True, null=True)
    per_client_limit = models.PositiveSmallIntegerField(blank=True, null=True)

    # connections
    creator = models.ForeignKey(Leader, on_delete=models.SET_NULL, null=True)
    # -----------

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
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.type) + str(self.title)


class DiscountItem(models.Model):
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)

    # connections
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, models.PROTECT)
    adder = models.ForeignKey(Leader, on_delete=models.SET_NULL, null=True)
    # -----------

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.discount}: to product {self.product}'
