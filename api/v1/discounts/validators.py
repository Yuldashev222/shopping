from django.core.exceptions import ValidationError

from . import models as models_discount


def active_and_not_deleted_discount(discount_id):
    discount = models_discount.Discount.objects.get(pk=discount_id)
    if not discount.active_object():
        raise ValidationError('object is not active')


def not_all_product(discount_id):
    discount = models_discount.Discount.objects.get(pk=discount_id)
    if not discount.for_all_product:
        raise ValidationError('this discount is valid for all products')


def quota_available(discount_id):
    discount = models_discount.Discount.objects.get(pk=discount_id)
    if discount.remaining_discount_quantity and discount.remaining_discount_quantity < 1:
        raise ValidationError('no available quota left!')
