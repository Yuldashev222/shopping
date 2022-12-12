from datetime import date
from django.db.models import Q, F
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions

from api.v1.accounts.permissions import IsActive
from .models import Delivery
from .serializers import (
    DeliveryListSerializer,
    DeliveryRetrieveSerializer,
    DeliveryDashboardListSerializer,
    DeliveryDashboardRetrieveSerializer
)


class DeliveryReadOnlyAPIViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_fields = ['price', 'available_from_date', 'available_to_date']
    search_fields = ['title', 'info_on_delivery_time']
    ordering = '-date_updated'
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'list':
            return DeliveryListSerializer
        return DeliveryRetrieveSerializer

    def get_queryset(self):
        queryset = Delivery.objects.exclude(
            Q(is_active=False) | Q(is_deleted=True) |
            Q(available_to_date__isnull=False) & Q(available_to_date__lt=date.today())
        )
        return queryset


class DeliveryAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsActive, IsAdminUser, DjangoModelPermissions]

    filterset_fields = [
        'creator', 'creator_detail_on_delete', 'date_created',
        'price', 'available_from_date', 'available_to_date'
    ]
    search_fields = ['title', 'info_on_delivery_time']
    ordering = '-date_updated'

    def get_queryset(self):
        queryset = Delivery.active_objects.select_related('creator', 'creator_detail_on_delete')
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return DeliveryDashboardListSerializer
        return DeliveryDashboardRetrieveSerializer
