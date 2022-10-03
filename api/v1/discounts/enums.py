from enum import Enum


class DiscountType(Enum):
    coupon = 'coupon'
    discount = 'discount'
    summa = 'summa'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)

