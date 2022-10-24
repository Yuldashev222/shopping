from django.urls import path, include

from api.v1.products import (
    views,
    routers
)

urlpatterns = [
    path('', include(routers.router.urls)),
]
