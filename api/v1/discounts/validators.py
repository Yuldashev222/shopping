from django.core.exceptions import ValidationError

from . import models as models_discount


def active_and_not_deleted_discount(discount_id):
    discount = models_discount.Discount.objects.get(pk=discount_id)
    if not discount.is_active or not discount.is_deleted:
        raise ValidationError('object is not active')
