from enum import Enum


class DeliveryStatuses(Enum):
    order_processing = 'order processing'
    pre_production = 'pre production'
    in_production = 'in production'
    shipped = 'shipped'
    delivered = 'delivered'
    failed = 'failed'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
