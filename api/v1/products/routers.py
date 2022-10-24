from rest_framework import routers

from api.v1.products.views import (
    colors,
    sizes,
    brands,
    categories,
    manufacturers
)

router = routers.SimpleRouter()

router.register('colors', colors.ProductColorAPIViewSet)
router.register('sizes', sizes.ProductSizeAPIViewSet)
router.register('brands', brands.ProductBrandAPIViewSet)
router.register('categories', categories.ProductCategoryAPIViewSet)
router.register('manufacturers', manufacturers.ProductManufacturerAPIViewSet)
