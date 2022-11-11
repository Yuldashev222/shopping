from rest_framework import (
    viewsets,
    mixins,
    status,
    response,
    permissions as rest_permissions
)

from api.v1.general.permissions import IsStaff, IsClient, IsOwnerClient
from .models import Order, OrderItem
from .serializers import OrderItemSerializer
from .permissions import IsOwnerOrderClient


class OrderItemAPIViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [rest_permissions.IsAuthenticated, IsClient, IsOwnerOrderClient]

    def filter_queryset(self, queryset):
        print(self.request.user.phone_number)
        queryset = queryset.filter(order__client_id=self.request.user.id)
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
