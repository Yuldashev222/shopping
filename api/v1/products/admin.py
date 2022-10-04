from django.contrib import admin


from .models import (
    Brand,
    Category,
    Manufacturer,
    ProductImages,
    Product,
    ProductAsterisk,
    ProductColor,
    AddToProduct
 )


admin.site.register(
    [Brand, Category, Manufacturer, ProductImages, Product, ProductAsterisk, ProductColor, AddToProduct]
)
