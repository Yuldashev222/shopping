from django.db import models
from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField
from colorfield.fields import ColorField

from api.v1.accounts import models as account_models
from api.v1.carts.models import Cart
from api.v1.discounts.models import Discount
from api.v1.wishlists.models import Wishlist
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

    exclude_discount = models.ForeignKey(Discount, models.SET_NULL, null=True, blank=True)

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
    main_image = models.ImageField(upload_to='Products/images/', help_text='main image', blank=True, null=True)
    image1 = models.ImageField(upload_to='Products/images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='Products/images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='Products/images/', blank=True, null=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class Product(models.Model):
    name = models.CharField(max_length=255)
    count_in_stock = models.PositiveSmallIntegerField(default=1, help_text='how many do you want to add?')

    desc = models.TextField(max_length=1500, blank=True, null=True)
    price = models.PositiveIntegerField()

    size = models.CharField(max_length=4, choices=ProductSizes.choices())
    colors = models.ManyToManyField(ProductColor, related_name='products')
    department = models.CharField(max_length=3, choices=ProductDepartments.choices())

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    available_from_date = models.DateTimeField(blank=True, null=True,
                                               help_text='from what date the product is available')
    available_to_date = models.DateTimeField(blank=True, null=True, help_text='until when is the product available')

    delivery_service = models.BooleanField(default=False)
    delivery_time = models.IntegerField(help_text='enter how many days it will be delivered!',
                                        blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    tags = TaggableManager()

    image = models.ForeignKey(ProductImages, on_delete=models.SET_NULL, null=True,
                              related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True,
                              related_name='products')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name='products')
    creator = models.ForeignKey(account_models.Vendor, models.SET_NULL, blank=True, null=True,
                                related_name='products')
    discount = models.ForeignKey(Discount, models.SET_NULL, null=True, blank=True,
                                 related_name='products')
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True,
                             related_name='products')
    wishlist = models.ForeignKey(Wishlist, on_delete=models.SET_NULL, null=True,
                                 related_name='products')

    def __str__(self):
        return self.name


class ProductAsterisk(models.Model):
    asterisks = models.SmallIntegerField(choices=ProductAsterisks.choices())

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Asterisks in {self.product}'
