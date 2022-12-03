from rest_framework import (
    viewsets,
    response,
)

from api.v1.general.filters import ActiveAndNotDeletedObjectFilterBackend
from .models import Delivery
from .serializers import DeliverySerializer


class DeliveryAPIViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.filter(is_active=True, is_deleted=False)
    serializer_class = DeliverySerializer
    # filter_backends = [ActiveAndNotDeletedObjectFilterBackend]

    def get_permissions(self):
        if self.action == 'list':
            pass
        return []
