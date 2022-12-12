from enum import Enum


class CustomUserRole(Enum):
    manager = 'manager'
    client = 'client'
    vendor = 'vendor'
    director = 'director'
    developer = 'developer'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
