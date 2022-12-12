from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Shopping API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://t.me/yuldashev222/",
        contact=openapi.Contact(email="oybekyuldashov54@gmail.com"),
        license=openapi.License(name="UZB License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    # swagger urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # shopping urls
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('api.v1.accounts.urls')),
    path('api/v1/deliveries/', include('api.v1.delivery.urls')),
    path('api/v1/products/', include('api.v1.products.urls')),
    path('api/v1/wishlists/', include('api.v1.wishlists.urls')),
    path('api/v1/orders/', include('api.v1.orders.urls'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path('debug/', include(debug_toolbar.urls)),

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
