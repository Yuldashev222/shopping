from datetime import date
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.accounts.models import UserDetailOnDelete
from api.v1.products.models import ProductItem, Product, ProductManufacturer, Brand, ProductCategory
from api.v1.products.validators import (
    active_and_not_deleted_product_item,
    active_and_not_deleted_product,
    active_manufacturer,
    active_and_not_deleted_brand,
    active_and_not_deleted_category
)
from api.v1.accounts.validators import is_manager_or_director, active_and_not_deleted_user
from api.v1.general.validators import validate_date
from api.v1.discounts.validators import active_and_not_deleted_discount, not_all_product, quota_available

from .enums import DiscountType
from .services import upload_location_discount_file, upload_location_discount_image


class Discount(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True, max_length=10000)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices())
    start_date = models.DateField(blank=True, null=True, validators=[validate_date])
    end_date = models.DateField(blank=True, null=True, validators=[validate_date])
    per_client_limit = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    discount_quantity = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    remaining_discount_quantity = models.PositiveIntegerField(blank=True, null=True)
    for_all_product = models.BooleanField(default=False)

    # additional fields
    file = models.FileField(upload_to=upload_location_discount_file, blank=True, null=True)
    image = models.ImageField(upload_to=upload_location_discount_image, blank=True, null=True)

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_manager_or_director],
    )
    creator_detail_on_delete = models.ForeignKey(
        UserDetailOnDelete, on_delete=models.PROTECT,
        blank=True, null=True
    )
    # -----------

    # discount types
    # 1 - discount price example: -10$, -20$, ...
    price = models.FloatField(validators=[MinValueValidator(0.1)], blank=True, null=True)

    # 2 - discount percent example: -10%, -20%, ...
    percent = models.FloatField(validators=[MinValueValidator(0.01)], blank=True, null=True)

    # 3 - free delivery service
    free_delivery = models.BooleanField(default=False)

    # 4 - if you make a minimum purchase of 100 dollars, you will get one of the 3 discounts above
    minimum_purchase = models.FloatField(validators=[MinValueValidator(1)], blank=True, null=True)

    # 5 - Buy n items and get the (n + 1)th free!
    quantity_to_free_quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], blank=True, null=True
    )
    free_quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    # --------------------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.discount_type}: {self.title[:25]}'

    def clean(self):
        errors = dict()

        if self.creator and self.creator_detail_on_delete:
            raise ValidationError({'creator_detail_on_delete': 'cannot be this field when the "creator" field exists'})

        if self.for_all_product and (self.discount_quantity or self.remaining_discount_quantity):
            raise ValidationError('the "for_all_product" following two fields "discount_quantity",'
                                  ' "remaining_discount_quantity" must not exist when this field is present')

        if self.end_date and self.end_date <= date.today():
            errors['end_date'] = ['"date" must be greater than today\'s date!']

        if self.end_date and not self.start_date:
            self.start_date = date.today()

        if (
                self.quantity_to_free_quantity and not self.free_quantity or
                self.free_quantity and not self.quantity_to_free_quantity
        ):
            raise ValidationError(
                {'quantity_to_free_quantity': '"free_quantity" field not null',
                 'free_quantity': '"quantity_to_free_quantity" field not null'}
            )

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

        if self.discount_type == DiscountType.minimum_purchase.name:
            if self.quantity_to_free_quantity:
                raise ValidationError({'quantity_to_free_quantity': 'for the "minimum_purchase" field. '
                                                                    'The "quantity_to_free_quantity" field must be empty'})

            if self.free_delivery and self.price and self.percent:
                raise ValidationError('Choose one of the 3 fields: "free_delivery", "price", "percent"')

            if self.price and self.percent:
                raise ValidationError('Choose one of the 2 fields: "price", "percent"')

            if self.free_delivery and self.percent:
                raise ValidationError('Choose one of the 2 fields: "free_delivery", "percent"')

            if self.free_delivery and self.price:
                raise ValidationError('Choose one of the 2 fields: "free_delivery", "price"')

    def active_object(self):
        if self.end_date and self.end_date < date.today():
            return False
        return self.is_active and not self.is_deleted


class DiscountItem(models.Model):
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)

    # connections
    discount = models.ForeignKey(
        Discount, models.PROTECT,
        validators=[active_and_not_deleted_discount, not_all_product, quota_available]
    )
    product_item = models.ForeignKey(
        ProductItem, on_delete=models.CASCADE, blank=True, null=True,
        validators=[active_and_not_deleted_product_item]
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True,
        validators=[active_and_not_deleted_product]
    )
    manufacturer = models.ForeignKey(
        ProductManufacturer, on_delete=models.CASCADE,
        validators=[active_manufacturer], blank=True, null=True
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, null=True, blank=True,
        validators=[active_and_not_deleted_brand]
    )
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, blank=True, null=True,
        validators=[active_and_not_deleted_category]
    )
    adder = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, validators=[active_and_not_deleted_user, is_manager_or_director],
    )
    adder_detail_on_delete = models.ForeignKey(
        UserDetailOnDelete, on_delete=models.PROTECT,
        blank=True, null=True
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

    class Meta:
        unique_together = [
            ['discount', 'product'],
            ['discount', 'product_item'],
            ['discount', 'manufacturer'],
            ['discount', 'brand'],
            ['discount', 'category']
        ]  # last

    def clean(self):
        errors = dict()

        if self.adder and self.adder_detail_on_delete:
            errors['adder_detail_on_delete'] = ['cannot be this field when the "adder" field exists']

        if self.discount.end_date and self.discount.end_date < date.today():
            errors['discount'] = ['this promotion has expired!']

        if errors:
            raise ValidationError(errors)

        if self.product_item and self.product:
            raise ValidationError('product and product item choose one of the two')

        if not (self.product_item or self.product):
            raise ValidationError('it is mandatory to choose one of the two')

        if (
                self.quantity and
                self.discount.remaining_discount_quantity and
                self.quantity > self.discount.remaining_discount_quantity
        ):
            raise ValidationError({'quantity': 'more than the specified discount quantity'})

    def active_object(self):
        return self.is_active and not self.is_deleted
