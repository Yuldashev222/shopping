from datetime import date
from django.db import models
from django.core.exceptions import ValidationError

from api.v1.accounts.models import CustomUser
from api.v1.products.models import ProductItem, Product
from api.v1.accounts.validators import leader_user
from .enums import DiscountType
from .services import upload_location_discount_file, upload_location_discount_image
from api.v1.general.validators import validate_date


class Discount(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices())
    start_date = models.DateField(blank=True, null=True, validators=[validate_date])
    end_date = models.DateField(blank=True, null=True, validators=[validate_date])
    per_client_limit = models.PositiveSmallIntegerField(blank=True, null=True)
    discount_quantity = models.PositiveIntegerField(blank=True, null=True)

    # additional fields
    file = models.FileField(upload_to=upload_location_discount_file, blank=True, null=True)
    image = models.ImageField(upload_to=upload_location_discount_image, blank=True, null=True)

    # connections
    creator = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        validators=[leader_user],
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    # -----------

    # discount types
    # 1 - discount price example: -10$, 20$, ...
    price = models.PositiveIntegerField(blank=True, null=True)

    # 2 - discount percent example: -10%, -20%, ...
    percent = models.PositiveIntegerField(blank=True, null=True)

    # 3 - Buy n items and get the (n + 1)th free!
    quantity_to_free_quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    free_quantity = models.PositiveSmallIntegerField(blank=True, null=True)

    # 4 - free delivery service
    free_delivery = models.BooleanField(default=False)

    # 5 - if you make a minimum purchase of 100 dollars, you will get one of the 4 discounts above
    minimum_purchase = models.PositiveIntegerField(blank=True, null=True)

    # --------------------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.discount_type) + str(self.title)[:15]

    def clean(self):
        errors = dict()

        if self.end_date and not self.start_date:
            self.start_date = date.today()

        if self.start_date and self.end_date:
            if self.end_date <= date.today():
                errors['end_date'] = ['end_date must be greater than today date']
            if self.end_date <= self.start_date:
                errors['end_date'] = ['end_date must be greater than start_date']

        if (
                (self.discount_type == DiscountType.price.name) and
                (
                        self.percent or
                        self.quantity_to_free_quantity or
                        self.free_delivery or
                        self.minimum_purchase
                )
        ):
            raise ValidationError({'price': 'select only the "price" field if the type is "price"'})

        if (
                (self.discount_type == DiscountType.percent.name) and
                (
                        self.price or
                        self.quantity_to_free_quantity or
                        self.free_delivery or
                        self.minimum_purchase
                )
        ):
            raise ValidationError({'percent': 'select only the "percent" field if the type is "percent"'})

        if (
                (self.discount_type == DiscountType.by_quantity.name) and
                (
                        self.price or
                        self.percent or
                        self.free_delivery or
                        self.minimum_purchase
                )
        ):
            raise ValidationError({'by_quantity': 'select only the "by_quantity" field if the type is "by_quantity"'})

        if (
                (self.discount_type == DiscountType.free_delivery.name) and
                (
                        self.price or
                        self.percent or
                        self.quantity_to_free_quantity or
                        self.minimum_purchase
                )
        ):
            raise ValidationError(
                {'free_delivery': 'select only the "free_delivery" field if the type is "free_delivery"'})

        if (
                (self.discount_type == DiscountType.minimum_purchase.name) and
                (
                        self.price or
                        self.percent or
                        self.quantity_to_free_quantity or
                        self.free_delivery
                )
        ):
            raise ValidationError(
                {'minimum_purchase': 'select only the "minimum_purchase" field if the type is "minimum_purchase"'})

    def active_object(self):
        return self.is_active and not self.is_deleted


class DiscountItem(models.Model):
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)

    # connections
    discount = models.ForeignKey(
        Discount,
        models.PROTECT,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    product_item = models.ForeignKey(
        ProductItem,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    adder = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        validators=[leader_user],
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    # -----------

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        if self.product:
            return f'{self.product}: to discount {self.discount}'
        return f'{self.product_item}: to discount {self.discount}'

    def clean(self):
        if self.product_item and self.product:
            raise ValidationError('product and product item choose one of the two')

        if not (self.product_item or self.product):
            raise ValidationError('it is mandatory to choose one of the two')

    class Meta:
        unique_together = [['discount', 'product'], ['discount', 'product_item']]  # last

    def active_object(self):
        return self.is_active and not self.is_deleted
