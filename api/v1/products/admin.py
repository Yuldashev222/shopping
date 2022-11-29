from django.contrib import admin

from .models import (
    ProductColor,
    ProductSize,
    Brand,
    ProductCategory,
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
        ProductCategory,
        ProductManufacturer,
        Product,
        ProductItem,
        ProductStar,
        ProductComment
    ]
)
