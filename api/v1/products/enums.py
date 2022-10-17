from enum import Enum


class ProductDepartments(Enum):
    m = 'man'
    w = 'woman'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)


class ProductStars(Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
