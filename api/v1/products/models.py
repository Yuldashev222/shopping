from django.db import models
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from datetime import date

from api.v1.accounts import models as account_models
from api.v1.delivery.models import Delivery
from api.v1.general.validators import active_relation
from .enums import ProductDepartments, ProductStars
from .services import upload_location_product_image
from .validators import validate_color_hexa


class ProductColor(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    hexa = models.CharField(max_length=9, validators=[validate_color_hexa], unique=True, db_index=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        #  ------------------------------------------------
        return f'{self.hexa}: {self.name}'

    class Meta:
        ordering = ('name',)


class ProductSize(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    desc = models.CharField(max_length=500, blank=True, null=True)

    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class ProductManufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    desc = models.TextField(max_length=2000, blank=True)

    # connections
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(account_models.Staff, models.SET_NULL, null=True)
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    name = models.CharField(max_length=400)
    desc = models.TextField(max_length=1500, blank=True)
    price = models.PositiveIntegerField(help_text='enter the price in dollars.')
    department = models.CharField(max_length=1, choices=ProductDepartments.choices())
    count_in_stock = models.PositiveSmallIntegerField(default=1, help_text='how many do you want to add?')
    count_booked = models.PositiveSmallIntegerField(default=0)
    count_sold = models.PositiveIntegerField(default=0)
    available_from_date = models.DateField(
        blank=True,
        null=True,
        help_text='from what date the product is available'
    )
    available_to_date = models.DateField(
        blank=True,
        null=True,
        help_text='until when is the product available'
    )
    tags = TaggableManager(blank=True)

    # connections
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, blank=True, null=True, validators=[active_relation])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, validators=[active_relation])
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, validators=[active_relation])
    manufacturer = models.ForeignKey(ProductManufacturer, on_delete=models.SET_NULL, null=True, blank=True, validators=[active_relation])
    size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, validators=[active_relation])
    color = models.ForeignKey(ProductColor, on_delete=models.PROTECT, validators=[active_relation])
    creator = models.ForeignKey(account_models.Staff, models.SET_NULL, null=True, validators=[active_relation])
    # -----------

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}. price: {self.price}'

    def clean(self):
        errors = dict()

        #  count_in_stock and count_booked validations
        if self.count_in_stock < self.count_booked:
            errors['count_booked'] = ['the number of products being booked must not exceed the number of products in stock!']

        #  available_to_date and available_from_date validations ---------------
        today_date = date.today()
        if self.available_from_date and self.available_to_date:
            if self.available_from_date < today_date:
                errors['available_from_date'] = ['the available date must not be less than today\'s date']
            if self.available_from_date >= self.available_to_date:
                errors['available_to_date'] = ['the available from data must be less than the to date']

        elif self.available_from_date and self.available_from_date < today_date:
            errors['available_from_date'] = ['the available date must not be less than today\'s date']

        elif self.available_to_date:
            if self.available_to_date <= today_date:
                errors['available_to_date'] = ['the available to data must be to day date']
            else:
                self.available_from_date = today_date
        #  ------------------------------------------------

        if errors:
            raise ValidationError(errors)


class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_location_product_image, validators=[])
    is_main = models.BooleanField(default=False)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True, editable=False)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        constraints = (
            models.UniqueConstraint(
                name='unique_product_main_image',
                fields=['product'],
                condition=models.Q(is_main=True)
            ),
        )


class ProductStar(models.Model):
    star = models.PositiveSmallIntegerField(choices=ProductStars.choices())

    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    client = models.ForeignKey(account_models.Client, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.client:
            return f'{self.client}: {self.star} stars'
        return f'{self.star} stars'

    class Meta:
        unique_together = ['product', 'client']  # ???


class ProductComment(models.Model):
    text = models.CharField(max_length=400)

    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    client = models.ForeignKey(account_models.Client, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.client}: {str(self.text).strip()[:30]}'
