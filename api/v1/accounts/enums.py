from enum import Enum


class CustomUserRoles(Enum):
    manager = 'manager'
    client = 'client'
    vendor = 'vendor'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)

