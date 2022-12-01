from django.core.exceptions import ValidationError

from . import models as order_models


def not_confirmed(order_id):
    order = order_models.Order.objects.get(pk=order_id)
    if order.is_confirmed:
        raise ValidationError('This order is pre-approved')


def active_and_not_deleted_order(order_id):
    order = order_models.Order.objects.get(pk=order_id)
    if not order.active_object():
        raise ValidationError('object is not active')
