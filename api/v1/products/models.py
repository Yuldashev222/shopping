from django.db import models
from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField
from colorfield.fields import ColorField

from api.v1.accounts import models as account_models
from .enums import ProductSizes, ProductDepartments, ProductAsterisks


class ProductColor(models.Model):
    name = models.CharField(max_length=50)
    color = ColorField(format='hexa')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    # exclude_discount = models.ForeignKey(Discount, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProductImages(models.Model):
    main_image = models.ImageField(upload_to='Products/images/', help_text='main image', null=True)
    image1 = models.ImageField(upload_to='Products/images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='Products/images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='Products/images/', blank=True, null=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class Product(models.Model):
    name = models.CharField(max_length=255)

    desc = models.TextField(max_length=1500, blank=True, null=True)

    department = models.CharField(max_length=1, choices=ProductDepartments.choices())

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    is_active = models.BooleanField(default=True)

    tags = TaggableManager()

    image = models.ForeignKey(ProductImages, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True,
                              related_name='products')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name='products')
    creator = models.ForeignKey(account_models.Vendor, models.SET_NULL, null=True,
                                related_name='products')

    def __str__(self):
        return self.name


class AddToProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=4, choices=ProductSizes.choices())
    price = models.PositiveIntegerField(help_text='enter the price in dollars.')
    color = models.ForeignKey(ProductColor, on_delete=models.PROTECT, related_name='products')

    count_in_stock = models.PositiveSmallIntegerField(default=1, help_text='how many do you want to add?')
    count_booked = models.PositiveSmallIntegerField(default=0)
    count_sold = models.PositiveIntegerField(default=0)

    creator = models.ForeignKey(account_models.Vendor, models.SET_NULL, null=True, )

    delivery_service = models.BooleanField(default=False)
    delivery_time = models.IntegerField(help_text='enter how many days it will be delivered!',
                                        blank=True, null=True)

    available_from_date = models.DateTimeField(blank=True, null=True,
                                               help_text='from what date the product is available')
    available_to_date = models.DateTimeField(blank=True, null=True,
                                             help_text='until when is the product available')

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)


class ProductAsterisk(models.Model):
    asterisks = models.SmallIntegerField(choices=ProductAsterisks.choices())

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Asterisks in {self.product}'
