from rest_framework.routers import SimpleRouter

from .views.user_detail_on_delete import DeletedUserDataAPIViewSet

router = SimpleRouter()

router.register('deleted', DeletedUserDataAPIViewSet, basename='deleted-user')
