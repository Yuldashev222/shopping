from rest_framework import routers

from api.v1.accounts.views.all_users import UserAPIViewSet

router = routers.SimpleRouter()

router.register('', UserAPIViewSet)


