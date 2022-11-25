from django.core.exceptions import ValidationError

from .models import Delivery


def active_and_not_deleted_delivery(delivery_id):
    delivery = Delivery.objects.get(pk=delivery_id)
    if not delivery.is_active or delivery.is_deleted:
        raise ValidationError('object is not active')
