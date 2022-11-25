from enum import Enum


class ProductDepartments(Enum):
    m = 'man'
    w = 'woman'

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)


class ProductStars(Enum):
    one = 1
    one_half = 1.5
    two = 2
    two_half = 2.5
    three = 3
    three_half = 3.5
    four = 4
    four_half = 4.5
    five = 5

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
