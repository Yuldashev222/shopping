from rest_framework import routers

from .views import OrderItemAPIViewSet

router = routers.SimpleRouter()
router.register('items', OrderItemAPIViewSet)
