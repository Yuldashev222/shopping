from django.urls import path, include

from .views import (
    clients,
    staffs,
    forgot_reset_change_password,
    retrieve_update_destroy,
    login_logout_register
)
from .routers import router

urlpatterns = [
    path('login/', login_logout_register.LoginAPIView.as_view(), name='user-login'),
    path('logout/', login_logout_register.user_logout),
    path('clients/register/', login_logout_register.ClientRegisterAPIView.as_view()),
    path('staffs/register/', login_logout_register.StaffRegisterAPIView.as_view()),
    path('auth/', include('rest_framework.urls')),  # last

    # passwords
    path('forgot-password/', forgot_reset_change_password.forgot_password),
    path('reset-password/', forgot_reset_change_password.reset_password, name='reset-password'),
    path('change-password/', forgot_reset_change_password.change_password),

    # get users
    path('me/', retrieve_update_destroy.OwnerUserRetrieveUpdateDestroyAPIView.as_view(), name='user-profile'),
    path('clients/', clients.ClientListAPIView.as_view(), name='client-list'),
    path('staffs/', staffs.StaffListAPIView.as_view(), name='staff-list'),
    path('<int:pk>/', retrieve_update_destroy.StaffRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    path('', include(router.urls))

]
