from django.db import models
from taggit.managers import TaggableManager

from api.v1.accounts import models as account_models
from api.v1.delivery.models import Delivery
from .enums import ProductDepartments, ProductStars
from .services import upload_location_product_image
from .validators import validate_color_hexa


class ProductColor(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    hexa = models.CharField(max_length=9, validators=[validate_color_hexa], unique=True, db_index=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
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
    desc = models.TextField(max_length=1500, blank=True)

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
    delivery_service = models.BooleanField(default=False)
    available_from_date = models.DateTimeField(blank=True, null=True,
                                               help_text='from what date the product is available')
    available_to_date = models.DateTimeField(blank=True, null=True,
                                             help_text='until when is the product available')
    tags = TaggableManager(blank=True)

    # connections
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    manufacturer = models.ForeignKey(ProductManufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.PROTECT)
    color = models.ForeignKey(ProductColor, on_delete=models.PROTECT)
    creator = models.ForeignKey(account_models.Staff, models.SET_NULL, null=True)
    # -----------

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}. price: {self.price}'


class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_location_product_image, validators=[])
    is_main = models.BooleanField(default=False)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        unique_together = ['is_main', 'product']


class ProductStar(models.Model):
    star = models.PositiveSmallIntegerField(choices=ProductStars.choices())

    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    client = models.ForeignKey(account_models.Client, on_delete=models.SET_NULL, null=True, blank=True)

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

    def __str__(self):
        return f'{self.client}: {str(self.text).strip()[:30]}'
