from django.urls import path, include

from . import views, routers

urlpatterns = [
    path('', include(routers.router.urls)),
    # path('', views.WishlistListAPIView.as_view()),
]
