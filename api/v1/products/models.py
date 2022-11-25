from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError

from api.v1.accounts import models as account_models
from api.v1.accounts.validators import is_staff, active_and_not_deleted_user
from api.v1.delivery.models import Delivery
from api.v1.delivery.validators import active_and_not_deleted_delivery
from api.v1.products.validators import (
    active_category,
    active_and_not_deleted_product,
    active_brand,
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
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )

    def __str__(self):
        return f'{self.hexa}: {self.name}'

    def active_object(self):
        return self.is_active

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)


class ProductSize(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    desc = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )

    def __str__(self):
        return self.name

    def active_object(self):
        return self.is_active

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)


class Brand(models.Model):
    name = models.CharField(max_length=254, unique=True, db_index=True)

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    creator_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete,
        on_delete=models.PROTECT,
        blank=True, null=True
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError(
                {'creator_detail_on_delete': 'this field is automatically filled when the "creator" field is deleted'}
            )

    def active_object(self):
        return self.is_active

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    # connections
    parent = models.ForeignKey(
        'self', on_delete=models.PROTECT,
        blank=True, null=True,
        validators=[active_category],
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    creator_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete,
        on_delete=models.PROTECT,
        blank=True, null=True
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

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
        return self.is_active

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class ProductManufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
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
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    desc = models.TextField(max_length=2000, blank=True)
    tags = TaggableManager(blank=True)

    # connections
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, validators=[active_category]
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    creator_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete,
        on_delete=models.PROTECT,
        blank=True, null=True
    )
    # -----------

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
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)


class ProductItem(models.Model):
    name = models.CharField(max_length=400, blank=True, null=True)
    desc = models.TextField(max_length=1500, blank=True, null=True)
    price = models.DecimalField(max_digits=25, decimal_places=3)
    department = models.CharField(max_length=1, choices=ProductDepartments.choices())
    count_in_stock = models.PositiveSmallIntegerField(default=0, help_text='how many do you want to add?')
    count_booked = models.PositiveSmallIntegerField(default=0)
    count_sold = models.PositiveIntegerField(default=0)
    available_from_date = models.DateField(
        blank=True, null=True,
        help_text='from what date the product is available',
    )
    available_to_date = models.DateField(
        blank=True, null=True,
        help_text='until when is the product available',
    )
    tags = TaggableManager(blank=True)

    # connections
    delivery = models.ForeignKey(
        Delivery, on_delete=models.PROTECT,
        blank=True, null=True,
        validators=[active_and_not_deleted_delivery]
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT,
        validators=[active_and_not_deleted_product],
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT,
        null=True, blank=True,
        validators=[active_brand]
    )
    manufacturer = models.ForeignKey(
        ProductManufacturer,
        on_delete=models.PROTECT,
        blank=True, null=True,
        validators=[active_manufacturer]
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )
    creator_detail_on_delete = models.ForeignKey(
        account_models.UserDetailOnDelete,
        on_delete=models.PROTECT,
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
        return f'{self.name}. price: {self.price}'

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError(
                {'creator_detail_on_delete': 'this field is automatically filled when the "creator" field is deleted'}
            )

    def active_object(self):
        return self.is_active and not self.is_deleted

    class Meta:
        ordering = ['date_created', ]
        unique_together = ['department', 'product', 'brand', 'manufacturer', 'size', 'color']  # last
        constraints = [
            models.CheckConstraint(
                check=models.Q(count_in_stock__gte=models.F('count_booked')),
                name='the number of products being booked must not exceed the number of products in stock!'
            )
        ]


class ProductItemHistory(models.Model):
    quantity = models.PositiveSmallIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)

    product_item = models.ForeignKey(
        ProductItem, on_delete=models.CASCADE,
        validators=[active_and_not_deleted_product_item]
    )
    adder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff],
    )

    def __str__(self):
        return f'{self.quantity}>> {self.product_item}'


class ProductStar(models.Model):
    star = models.PositiveSmallIntegerField(choices=ProductStars.choices())

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
        Product,
        on_delete=models.CASCADE,
        validators=[active_and_not_deleted_product],
    )
    client = models.ForeignKey(
        account_models.Client,
        on_delete=models.SET_NULL, null=True,
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

    def active_object(self):
        return self.is_active and not self.is_deleted

    def clean(self):
        if self.client and self.client_detail_on_delete:
            raise ValidationError({'client_detail_on_delete': 'cannot be this field when the "client" field exists'})
