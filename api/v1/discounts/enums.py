from enum import Enum


class DiscountType(Enum):
    price = 'price'
    percent = 'percent'
    minimum_purchase = 'minimum purchase'
    by_quantity = 'by quantity'
    free_delivery = 'free delivery'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
