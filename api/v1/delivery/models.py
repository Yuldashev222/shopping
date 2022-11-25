from django.db import models
from django.core.exceptions import ValidationError

from django.conf import settings
from api.v1.accounts.models import UserDetailOnDelete
from api.v1.accounts.validators import is_staff, active_and_not_deleted_user

from .enums import DeliveryStatuses


class Delivery(models.Model):
    title = models.CharField(blank=True, null=True, max_length=400)
    price = models.PositiveIntegerField(default=0, help_text='enter the price in dollars.')
    delivery_time_in_hour = models.PositiveSmallIntegerField(
        help_text='enter how many hours it will be delivered!'
    )
    desc_for_delivery_time = models.CharField(max_length=400, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=DeliveryStatuses.choices(),
        default=DeliveryStatuses.order_processing.name,
    )

    # connections
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        validators=[active_and_not_deleted_user, is_staff]
    )
    creator_detail_on_delete = models.ForeignKey(
        UserDetailOnDelete,
        on_delete=models.PROTECT,
        blank=True, null=True
    )
    # -----------

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        if self.title:
            return f'{self.status}: {self.price}. {self.title}'
        return f'{self.status}: {self.price}'

    def clean(self):
        if self.creator and self.creator_detail_on_delete:
            raise ValidationError({'creator_detail_on_delete': 'cannot be this field when the "creator" field exists'})

    def active_object(self):
        return self.is_active and not self.is_deleted

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
