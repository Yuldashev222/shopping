from datetime import date
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from api.v1.accounts import models as account_models
from api.v1.accounts.validators import is_staff, active_and_not_deleted_user
from api.v1.delivery.models import Delivery
from api.v1.general.validators import validate_date
from api.v1.products.validators import (
    active_and_not_deleted_category,
    active_and_not_deleted_product,
    active_and_not_deleted_brand,
    active_manufacturer,
    active_product_size,
    validate_color_hexa,
    active_product_color,
    active_and_not_deleted_product_item
)

from .enums import ProductDepartments, ProductStars
from .services import upload_location_product_image


class ProductColor(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    hexa = models.CharField(max_length=9, validators=[validate_color_hexa], unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )

    def __str__(self):
        return f'{self.hexa}: {self.name}'

    def active_object(self):
        return self.is_active

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.name = self.name.strip().lower()

    class Meta:
        db_table = 'product_color'
        ordering = ('name',)


class ProductSize(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    desc = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )

    def __str__(self):
        return self.name

    def active_object(self):
        return self.is_active

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.name = self.name.strip().lower()

    class Meta:
        db_table = 'product_size'
        ordering = ('name',)


class ProductManufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def active_object(self):
        return self.is_active

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.name = self.name.strip().lower()

    class Meta:
        db_table = 'product_manufacturer'
        ordering = ('name',)


class Brand(models.Model):
    name = models.CharField(max_length=254, unique=True, db_index=True)

    # connections
    manufacturer = models.ForeignKey(
        ProductManufacturer, on_delete=models.PROTECT,
        validators=[active_manufacturer]
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    creator_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete,
        on_delete=models.PROTECT, blank=True, null=True
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError(
                {'creator_detail_on_delete': 'this field is automatically filled when the "creator" field is deleted'}
            )

    def active_object(self):
        return self.is_active and not self.is_deleted

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.name = self.name.strip().lower()

    class Meta:
        db_table = 'product_brand'
        ordering = ('name',)


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    # connections
    parent = models.ForeignKey(
        'self', on_delete=models.PROTECT, blank=True, null=True,
        validators=[active_and_not_deleted_category],
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    creator_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete,
        on_delete=models.PROTECT, blank=True, null=True
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError(
                {'creator_detail_on_delete': 'this field is automatically filled when the "creator" field is deleted'}
            )

    @classmethod
    def active_objects(cls):
        return cls.objects.filter(is_active=True)

    def active_object(self):
        return self.is_active and not self.is_deleted

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.name = self.name.strip().lower()

    class Meta:
        db_table = 'product_category'
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    desc = models.TextField(max_length=2000, blank=True)
    tags = TaggableManager(blank=True)

    # connections
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, validators=[active_and_not_deleted_category]
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    creator_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete, on_delete=models.PROTECT,
        blank=True, null=True
    )
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError(
                {'creator_detail_on_delete': 'this field is automatically filled when the "creator" field is deleted'}
            )

    def active_object(self):
        return self.is_active and not self.is_deleted

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.name = self.name.strip().lower()


class ProductItem(models.Model):
    name = models.CharField(max_length=400, blank=True, null=True)
    desc = models.TextField(max_length=1500, blank=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    department = models.CharField(max_length=1, choices=ProductDepartments.choices())
    count_in_stock = models.PositiveSmallIntegerField(default=0, help_text='how many do you want to add?')
    count_booked = models.PositiveSmallIntegerField(default=0)
    count_sold = models.PositiveIntegerField(default=0)
    available_from_date = models.DateField(
        validators=[validate_date], blank=True, null=True,
        help_text='from what date the product is available',
    )
    available_to_date = models.DateField(
        validators=[validate_date], blank=True, null=True,
        help_text='until when is the product available',
    )
    tags = TaggableManager(blank=True)

    # connections
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT,
        validators=[active_and_not_deleted_product],
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, null=True, blank=True,
        validators=[active_and_not_deleted_brand]
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    creator_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete, on_delete=models.PROTECT,
        blank=True, null=True
    )
    size = models.ForeignKey(
        ProductSize, on_delete=models.PROTECT,
        validators=[active_product_size]
    )
    color = models.ForeignKey(
        ProductColor, on_delete=models.PROTECT,
        validators=[active_product_color]
    )
    # -----------

    main_image = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True,
                                   help_text='This Main Image in Product')
    image1 = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True)
    image2 = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True)
    image3 = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True)
    image4 = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'${self.price}: {self.name}'

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError(
                {'creator_detail_on_delete': 'this field is automatically filled when the "creator" field is deleted'}
            )
        if self.available_to_date and self.available_to_date <= date.today():
            raise ValidationError({'available_to_date': '"date" must be greater than today\'s date!'})

    def active_object(self):
        return self.is_active and not self.is_deleted

    class Meta:
        db_table = 'product_item'
        ordering = ['date_created', ]
        unique_together = ['department', 'product', 'brand', 'size', 'color']  # last


class ProductItemHistory(models.Model):
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=1)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    product_item = models.ForeignKey(
        ProductItem, on_delete=models.CASCADE,
        validators=[active_and_not_deleted_product_item]
    )
    adder = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    adder_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete, on_delete=models.PROTECT,
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.quantity} >> {self.product_item}'

    class Meta:
        db_table = 'product_item_history'

    def clean(self):
        if self.adder and self.adder_detail_on_delete:
            raise ValidationError(
                {'adder_detail_on_delete': 'this field is automatically filled when the "adder" field is deleted'}
            )


class ProductStar(models.Model):
    star = models.FloatField(validators=[MinValueValidator(1)], choices=ProductStars.choices())

    # connections
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        validators=[active_and_not_deleted_product],
    )
    client = models.ForeignKey(
        account_models.Client, on_delete=models.SET_NULL,
        null=True, blank=True,
        validators=[active_and_not_deleted_user],
    )
    # ------------

    def __str__(self):
        if self.client:
            return f'{self.client}: {self.star} stars'
        return f'{self.star} stars'

    class Meta:
        db_table = 'product_star'
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'product'],
                name='client_product_unique_product_star'
            )
        ]


class ProductComment(models.Model):
    text = models.CharField(max_length=400)

    # connections
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        validators=[active_and_not_deleted_product],
    )
    client = models.ForeignKey(
        account_models.Client, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user],
    )
    client_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete,
        on_delete=models.PROTECT,
        blank=True, null=True
    )
    # ------------

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.client}: {str(self.text).strip()[:30]}'

    class Meta:
        db_table = 'product_comment'

    def active_object(self):
        return self.is_active and not self.is_deleted

    def clean(self):
        if self.client and self.client_detail_on_delete:
            raise ValidationError({'client_detail_on_delete': 'cannot be this field when the "client" field exists'})
