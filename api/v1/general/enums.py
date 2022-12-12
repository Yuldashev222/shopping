from enum import Enum


class Regions(Enum):
    ts = 'Tashkent City'
    tso = 'Tashkent Region'
    sr = 'Sirdaryo'
    jz = 'Jizzakh'
    sm = 'Samarkand'
    qs = 'Kashkadarya'
    srh = 'Surkhandarya'
    nv = 'Navoi'
    bx = 'Bukhara'
    kh = 'Khorezm'
    an = 'Andijan'
    fr = 'Fergana'
    nm = 'Namangan'
    kr = 'Karakalpakstan'

    @classmethod
    def choices(cls):
        return [[i.name, i.value] for i in cls]
