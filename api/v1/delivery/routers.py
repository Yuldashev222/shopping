from rest_framework.routers import DefaultRouter

from .views import DeliveryReadOnlyAPIViewSet, DeliveryAPIViewSet

router = DefaultRouter()

router.register('dashboard', DeliveryAPIViewSet, basename='delivery-dashboard')
router.register('', DeliveryReadOnlyAPIViewSet, basename='delivery')
