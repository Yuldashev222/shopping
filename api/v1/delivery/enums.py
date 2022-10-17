from enum import Enum


class DeliveryStatuses(Enum):
    order_processing = 'order_processing'
    pre_production = 'pre_production'
    in_production = 'in_production'
    shipped = 'shipped'
    delivered = 'delivered'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
