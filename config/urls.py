from django.contrib import admin
from django.urls import path

from send_email.views import send_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', send_email)
]
