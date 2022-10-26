from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from .views import (
    tokens,
    all_users,
    passwords,
    clients,
    managers,
    vendors,
)
from .routers import router

urlpatterns = [
    path('login/', tokens.LoginAPIView.as_view()),
    path('logout/', all_users.user_logout),
    path('clients/register/', clients.client_register),
    path('managers/register/', managers.manager_register),
    path('vendors/register/', vendors.vendor_register),

    # passwords
    path('forgot-password/', passwords.forgot_password),
    path('reset-password/<uidb64>/<token>/', passwords.reset_password),
    path('change-password/', passwords.change_password),

    # path('refresh/', TokenRefreshView.as_view()),
    # path('verify/', TokenVerifyView.as_view()),
    path('', include(router.urls)),
]
