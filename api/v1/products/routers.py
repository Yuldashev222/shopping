from rest_framework import routers

from api.v1.products.views import (
    colors,
    sizes,
    brands,
    categories,
    manufacturers,
    images,
    stars,
    comments,
    products,
    products_items
)

router = routers.SimpleRouter()

router.register('colors', colors.ProductColorAPIViewSet)
router.register('sizes', sizes.ProductSizeAPIViewSet)
router.register('brands', brands.ProductBrandAPIViewSet)
router.register('categories', categories.ProductCategoryAPIViewSet)
router.register('manufacturers', manufacturers.ProductManufacturerAPIViewSet)
router.register('images', images.ProductImageAPIViewSet)
router.register('stars', stars.ProductStarAPIViewSet)
router.register('comments', comments.ProductCommentAPIViewSet)
router.register('product_items', products_items.ProductItemAPIViewSet)
router.register('', products.ProductAPIViewSet)
