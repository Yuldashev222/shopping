from django.urls import path, include

from api.v1.products import routers as product_routers

urlpatterns = [
    path('', include(product_routers.router.urls)),
]
