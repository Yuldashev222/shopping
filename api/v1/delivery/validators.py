from django.core.exceptions import ValidationError

from . import models as delivery_models


def active_and_not_deleted_delivery(delivery_id):
    delivery = delivery_models.Delivery.objects.get(pk=delivery_id)
    if not delivery.active_object():
        raise ValidationError('object is not active')
