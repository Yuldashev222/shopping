from rest_framework import (
    viewsets,
    permissions as rest_permissions
)

from api.v1.accounts.permissions import IsClient
from .models import Order, OrderItem
from .serializers import OrderItemSerializer
from .permissions import IsOwnerOrderClient


class OrderItemAPIViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [rest_permissions.IsAuthenticated, IsClient, IsOwnerOrderClient]

    def get_queryset(self):
        queryset = OrderItem.objects.filter(order__client_id=self.request.user.id).select_related('product').all()
        return queryset
