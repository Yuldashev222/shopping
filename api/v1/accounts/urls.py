from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from .views.tokens import LoginAPIView
from .views.all_users import user_logout
from .views.passwords import forgot_password, reset_password, change_password
from .routers import router

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('logout/', user_logout),

    # passwords
    path('forgot-password/', forgot_password),
    path('reset-password/<uidb64>/<token>/', reset_password),
    path('change-password/', change_password),

    # path('refresh/', TokenRefreshView.as_view()),
    # path('verify/', TokenVerifyView.as_view()),
    path('', include(router.urls)),
]
