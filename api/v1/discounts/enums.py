from enum import Enum


class DiscountType(Enum):
    price = 'price'
    percent = 'percent'
    minimum_purchase = 'minimum_purchase'
    by_quantity = 'by_quantity'
    free_delivery = 'free_delivery'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
