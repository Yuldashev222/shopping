from rest_framework.routers import DefaultRouter

from .views import DeliveryAPIViewSet

router = DefaultRouter()

router.register('', DeliveryAPIViewSet)
