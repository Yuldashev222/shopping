from django.urls import path, include

from . import routers

urlpatterns = [
    path('', include(routers.router.urls)),
]
