from datetime import datetime

from django.db import models
from django.utils.timezone import now as datetime_now

from api.v1.accounts.models import Manager
from api.v1.products.models import AddToProduct
from . import enums


class Discount(models.Model):
    desc = models.CharField(max_length=1000)
    type = models.CharField(max_length=10, choices=enums.DiscountType.choices())
    start_date = models.DateTimeField(default=datetime_now)
    end_date = models.DateTimeField()
    per_limited_count = models.IntegerField(blank=True, null=True)
    per_customers_count = models.IntegerField(blank=True, null=True)
    delivery_service = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    coupon_code = models.IntegerField(blank=True, null=True)

    is_percent = models.BooleanField(default=True)
    percent = models.IntegerField(blank=True, null=True)

    min_sum = models.IntegerField(blank=True, null=True)
    max_sum = models.IntegerField(blank=True, null=True)

    creator = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)


class AddDiscountToProduct(models.Model):
    product = models.ForeignKey(AddToProduct, on_delete=models.PROTECT)
    discount = models.ForeignKey(Discount, models.PROTECT)
    count = models.PositiveSmallIntegerField(default=1)

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
