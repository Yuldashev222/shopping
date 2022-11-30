from rest_framework import routers

from .views import WishlistModelViewSet, WishlistListAPIView

router = routers.SimpleRouter()
router.register('dashboard', WishlistListAPIView, basename='wishlist-dashboard')
router.register('', WishlistModelViewSet, basename='wishlist')
