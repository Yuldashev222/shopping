from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.conf import settings
from api.v1.accounts.models import UserDetailOnDelete
from api.v1.orders.models import Order
from api.v1.accounts.validators import is_staff, active_and_not_deleted_user
from api.v1.orders.validators import active_and_not_deleted_order, not_confirmed

from .enums import DeliveryStatuses
from .services import upload_location_delivery_file, upload_location_delivery_image
from .validators import active_and_not_deleted_delivery


class Delivery(models.Model):
    title = models.CharField(blank=True, max_length=400)
    price = models.PositiveIntegerField(default=0, help_text='enter the price in dollars.')
    delivery_time_in_hour = models.FloatField(
        help_text='enter how many hours it will be delivered!',
        validators=[MinValueValidator(0.5)],
    )
    info_on_delivery_time = models.TextField(max_length=2000, blank=True)
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

    def __str__(self):
        if self.title:
            return f'${self.price} >> {self.title}'
        return f'${self.price}'

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError({'creator_detail_on_delete': 'cannot be this field when the "creator" field exists'})

    def active_object(self):
        return self.is_active and not self.is_deleted

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        self.delivery_time_in_hour = round(self.delivery_time_in_hour, 1)

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
