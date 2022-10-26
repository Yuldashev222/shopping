from rest_framework import routers

from api.v1.accounts.views.all_users import UserAPIViewSet
from api.v1.accounts.views.clients import ClientAPIViewSet

router = routers.SimpleRouter()

router.register('clients', ClientAPIViewSet)
router.register('', UserAPIViewSet)


