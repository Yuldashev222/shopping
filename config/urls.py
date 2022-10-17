from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from api.v1.accounts.models import CustomUser
# user = CustomUser.objects.create_superuser('+998912345679', 'director', 'asd', 'asd', password='1')
#
# print(user)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('api.v1.accounts.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
