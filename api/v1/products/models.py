from django.db import models
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
from datetime import date

from api.v1.accounts import models as account_models
from api.v1.general.services import date_from_today_date
from api.v1.delivery.models import Delivery
from api.v1.general.validators import active_relation
from .enums import ProductDepartments, ProductStars
from .services import upload_location_product_image
from .validators import validate_color_hexa


class ProductColor(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    hexa = models.CharField(max_length=9, validators=[validate_color_hexa], unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    # connections
    creator = models.ForeignKey(
        account_models.Staff,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )

    def __str__(self):
        return f'{self.hexa}: {self.name}'

    def active_object(self):
        return self.is_active

    class Meta:
        ordering = ('name',)


class ProductSize(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    desc = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # connections
    creator = models.ForeignKey(
        account_models.Staff,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )

    def __str__(self):
        return self.name

    def active_object(self):
        return self.is_active

    class Meta:
        ordering = ('name',)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    # connections
    creator = models.ForeignKey(
        account_models.Staff,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def active_object(self):
        return self.is_active

    class Meta:
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    # connections
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    creator = models.ForeignKey(
        account_models.Staff,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @classmethod
    def active_objects(cls):
        return cls.objects.filter(is_active=True)

    def active_object(self):
        return self.is_active

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class ProductManufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    # connections
    creator = models.ForeignKey(
        account_models.Staff,
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def active_object(self):
        return self.is_active

    class Meta:
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    desc = models.TextField(max_length=2000, blank=True)

    # connections
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_active': True})
    creator = models.ForeignKey(
        account_models.Staff,
        models.SET_NULL,
        null=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def active_object(self):
        return self.is_active and not self.is_deleted


class ProductItem(models.Model):
    name = models.CharField(max_length=400, blank=True)
    desc = models.TextField(max_length=1500, blank=True)
    price = models.PositiveIntegerField(help_text='enter the price in dollars.')
    department = models.CharField(max_length=1, choices=ProductDepartments.choices())
    count_in_stock = models.PositiveSmallIntegerField(default=0, help_text='how many do you want to add?')
    count_booked = models.PositiveSmallIntegerField(default=0)
    count_sold = models.PositiveIntegerField(default=0)
    available_from_date = models.DateField(
        blank=True,
        null=True,
        help_text='from what date the product is available',
    )
    available_to_date = models.DateField(
        blank=True,
        null=True,
        help_text='until when is the product available',
    )
    tags = TaggableManager(blank=True)

    # connections
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_active': True}
    )
    manufacturer = models.ForeignKey(
        ProductManufacturer,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={'is_active': True}
    )
    creator = models.ForeignKey(
        account_models.Staff,
        models.SET_NULL,
        null=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    size = models.ForeignKey(ProductSize, on_delete=models.PROTECT, limit_choices_to={'is_active': True})
    color = models.ForeignKey(ProductColor, on_delete=models.PROTECT, limit_choices_to={'is_active': True})
    # -----------

    main_image = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True,
                                   help_text='This Main Image in Product')
    image1 = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True)
    image2 = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True)
    image3 = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True)
    image4 = models.ImageField(upload_to=upload_location_product_image, blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}. price: {self.price}'

    def active_object(self):
        return self.is_active and not self.is_deleted

    class Meta:
        ordering = ['date_added', ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(count_in_stock__gte=models.F('count_booked')),
                name='the number of products being booked must not exceed the number of products in stock!'
            )
        ]

    # def clean(self):
    #     errors = dict()
    #
    #     #  count_in_stock and count_booked validations
    #     if self.count_in_stock < self.count_booked:
    #         errors['count_booked'] = [
    #             'the number of products being booked must not exceed the number of products in stock!']
    #
    #     #  available_to_date and available_from_date validations ---------------
    #     today_date = date.today()
    #     if self.available_from_date and self.available_to_date:
    #         if self.available_from_date >= self.available_to_date:
    #             errors['available_to_date'] = ['the available from data must be less than the to date']
    #
    #     elif self.available_to_date:
    #         if self.available_to_date <= today_date:
    #             errors['available_to_date'] = ['the available to data must be to day date']
    #         else:
    #             self.available_from_date = today_date
    #     #  ------------------------------------------------
    #
    #     if errors:
    #         raise ValidationError(errors)


class ProductStar(models.Model):
    star = models.PositiveSmallIntegerField(choices=ProductStars.choices())

    product = models.ForeignKey(
        ProductItem,
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    client = models.ForeignKey(
        account_models.Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.client:
            return f'{self.client}: {self.star} stars'
        return f'{self.star} stars'

    def active_object(self):
        return self.is_active

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'product'],
                name='client_product_unique_product_star'
            )
        ]


class ProductComment(models.Model):
    text = models.CharField(max_length=400)

    product = models.ForeignKey(
        ProductItem,
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    client = models.ForeignKey(
        account_models.Client,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.client}: {str(self.text).strip()[:30]}'

    def active_object(self):
        return self.is_active and not self.is_deleted
