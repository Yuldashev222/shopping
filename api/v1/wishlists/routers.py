from rest_framework import routers

from .views import WishlistModelViewSet, WishlistListRetrieveAPIView

router = routers.SimpleRouter()
router.register('dashboard', WishlistListRetrieveAPIView, basename='wishlist')
router.register('', WishlistModelViewSet, basename='wishlist')
