from enum import Enum


class OrderStatuses(Enum):
    success = 'success'
    pending = 'pending'
    cancelled = 'cancelled'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
