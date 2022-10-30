from django.db import models

from api.v1.accounts.models import Staff
from .enums import DeliveryStatuses


class Delivery(models.Model):
    title = models.CharField(blank=True, null=True, max_length=400)
    price = models.PositiveIntegerField(default=0, help_text='enter the price in dollars.')
    delivery_time_in_day = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='enter how many days it will be delivered!'
    )
    status = models.CharField(
        max_length=20,
        choices=DeliveryStatuses.choices(),
        default=DeliveryStatuses.order_processing.value,
    )

    # connections
    creator = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'is_active': True, 'is_deleted': False}
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

    def active_object(self):
        return self.is_active and not self.is_deleted

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
