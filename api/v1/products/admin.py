from django.contrib import admin

from .models import (
    ProductColor,
    ProductSize,
    Brand,
    Category,
    ProductManufacturer,
    Product,
    ProductItem,
    ProductStar,
    ProductComment
 )

admin.site.register(
    [
        ProductColor,
        ProductSize,
        Brand,
        Category,
        ProductManufacturer,
        Product,
        ProductItem,
        ProductStar,
        ProductComment
    ]
)
