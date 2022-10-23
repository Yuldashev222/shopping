from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from .views.tokens import LoginAPIView
from .views.passwords import forgot_password, reset_password
from .routers import router

urlpatterns = [
    path('login/', LoginAPIView.as_view()),

    # passwords
    path('forgot-password/', forgot_password),
    path('reset-password/<uidb64>/<token>/', reset_password),
    # path('refresh/', TokenRefreshView.as_view()),
    # path('verify/', TokenVerifyView.as_view()),
    path('', include(router.urls)),
]
