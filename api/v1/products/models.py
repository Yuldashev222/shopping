from django.db import models
from taggit.managers import TaggableManager

from api.v1.accounts import models as account_models
from api.v1.delivery.models import Delivery
from .enums import ProductDepartments, ProductStars


class ProductColor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex = models.CharField(max_length=9, help_text='hexa format. Example --> #FFFFFFFF', unique=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProductSize(models.Model):
    name = models.CharField(max_length=100, unique=True)

    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'


class ProductManufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProductImage(models.Model):
    main_image = models.ImageField(upload_to='Products/images/', help_text='main image')
    image1 = models.ImageField(upload_to='Products/images/', blank=True)
    image2 = models.ImageField(upload_to='Products/images/', blank=True)
    image3 = models.ImageField(upload_to='Products/images/', blank=True)
    creator = models.ForeignKey(account_models.Staff, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    desc = models.TextField(max_length=1500, blank=True)
    department = models.CharField(max_length=1, choices=ProductDepartments.choices())

    # connections
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(account_models.Staff, models.SET_NULL, null=True)
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    price = models.PositiveIntegerField(help_text='enter the price in dollars.')
    count_in_stock = models.PositiveSmallIntegerField(default=1, help_text='how many do you want to add?')
    count_booked = models.PositiveSmallIntegerField(default=0)
    count_sold = models.PositiveIntegerField(default=0)
    delivery_service = models.BooleanField(default=False)
    available_from_date = models.DateTimeField(blank=True, null=True, help_text='from what date the product is available')
    available_to_date = models.DateTimeField(blank=True, null=True, help_text='until when is the product available')
    tags = TaggableManager(blank=True)

    # connections
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, null=True, blank=True)
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


class ProductStar(models.Model):
    star = models.PositiveSmallIntegerField(choices=ProductStars.choices())

    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    client = models.ForeignKey(account_models.Client, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.client:
            return f'{self.client}: {self.star} stars'
        return f'{self.star} stars'


class ProductComment(models.Model):
    text = models.CharField(max_length=200)

    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    client = models.ForeignKey(account_models.Client, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.client:
            return str(self.client) + ':' + str(self.text).strip()[:30]
        return str(self.text).strip()[:30]
