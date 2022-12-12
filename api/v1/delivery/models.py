from datetime import date
from django.db import models
from django.urls import reverse
from django.db.models.manager import Manager
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.conf import settings
from api.v1.accounts.models import UserDetailOnDelete
from api.v1.orders.models import Order
from api.v1.accounts.validators import is_staff, active_and_not_deleted_user
from api.v1.orders.validators import active_and_not_deleted_order, not_confirmed

from .enums import DeliveryStatuses
from .managers import ActiveDeliveryManager
from .services import upload_location_delivery_file, upload_location_delivery_image
from .validators import active_and_not_deleted_delivery
from api.v1.general.validators import validate_date


class Delivery(models.Model):
    title = models.CharField(blank=True, max_length=400)
    price = models.FloatField(validators=[MinValueValidator(0)])
    delivery_time_in_hour = models.FloatField(
        help_text='enter how many hours it will be delivered!',
        validators=[MinValueValidator(0.5)],
    )
    info_on_delivery_time = models.TextField(max_length=2000, blank=True)
    available_from_date = models.DateField(
        validators=[validate_date], blank=True, null=True,
        help_text='from what date the product is available',
    )
    available_to_date = models.DateField(
        validators=[validate_date], blank=True, null=True,
        help_text='until when is the product available',
    )
    file = models.FileField(upload_to=upload_location_delivery_file, blank=True, null=True)
    image = models.ImageField(upload_to=upload_location_delivery_image, blank=True, null=True)

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff]
    )
    creator_detail_on_delete = models.ForeignKey(
        UserDetailOnDelete, on_delete=models.PROTECT, blank=True, null=True
    )
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    active_objects = ActiveDeliveryManager()
    objects = Manager()

    def __str__(self):
        if self.title:
            return f'${self.price} >> {self.title}'
        return f'${self.price}'

    def get_creator_full_name(self):
        if self.creator:
            return self.creator.get_full_name()
        return self.creator_detail_on_delete.get_full_name()

    def get_creator_url(self):
        if self.creator:
            return reverse('user-detail', kwargs={'pk': self.creator.pk})
        return reverse('deleted-user-detail', kwargs={'pk': self.creator_detail_on_delete.pk})

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError({'creator_detail_on_delete': 'cannot be this field when the "creator" field exists'})

        if self.available_to_date and self.available_to_date <= date.today():
            raise ValidationError({'available_to_date': '"date" must be greater than today\'s date!'})

        if self.available_to_date and self.available_from_date and self.available_to_date < self.available_from_date:
            print(self.available_from_date, self.available_to_date)
            raise ValidationError({'available_to_date': 'must be greater than "available_from_date"'})

        if self.available_to_date and not self.available_from_date:
            self.available_from_date = date.today()

    @property
    def active_object(self):
        bol = self.is_active and not self.is_deleted
        if self.available_to_date:
            return bol and self.available_to_date <= date.today()
        return bol

    def save(self, *args, **kwargs):
        self.delivery_time_in_hour = round(self.delivery_time_in_hour, 1)
        super().save(*args, *kwargs)

    class Meta:
        db_table = 'delivery'
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'


class DeliveryOrder(models.Model):
    status = models.CharField(
        max_length=20, choices=DeliveryStatuses.choices(), default=DeliveryStatuses.order_processing.name,
    )
    order = models.OneToOneField(
        Order, on_delete=models.PROTECT, validators=[active_and_not_deleted_order, not_confirmed]
    )
    delivery = models.ForeignKey(
        Delivery, on_delete=models.PROTECT, validators=[active_and_not_deleted_delivery]
    )

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order} >> {self.status}'

    class Meta:
        db_table = 'delivery_order'
        verbose_name = 'Order Delivery'
        verbose_name_plural = 'Order Deliveries'

    def active_object(self):
        return self.is_active and not self.is_deleted
