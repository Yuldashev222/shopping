from django.http import Http404
from django.core.exceptions import ValidationError
from rest_framework import (
    viewsets,
    mixins,
    status,
    response,
    permissions as rest_permissions
)

from api.v1.accounts.permissions import IsStaff, IsClient
from api.v1.accounts.models import Client
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistListSerializer


class WishlistModelViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [rest_permissions.IsAuthenticated, IsClient]
    filterset_fields = ['product_item', 'date_added']
    search_fields = ['product_item__name']
    ordering_fields = ['date_added', 'product_item__name']
    ordering = '-date_added'

    def get_queryset(self):
        queryset = Wishlist.objects.filter(
            client_id=self.request.user.id
        ).select_related('product_item', 'product_item__product')
        return queryset

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            if len(request.data) > 20:
                return response.Response(
                    {'detail': ['You must send a maximum of 20 objects!']},
                    status=status.HTTP_207_MULTI_STATUS
                )
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WishlistListAPIView(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = WishlistListSerializer
    permission_classes = [rest_permissions.IsAuthenticated, IsStaff]
    filterset_fields = ['product_item__product', 'product_item', 'client', 'date_added']
    search_fields = ['client__phone_number', 'client__email', 'client__first_name', 'client__last_name']
    ordering_fields = ['date_added', 'product_item__name', 'product_item__product__name']
    ordering = '-date_added'
    lookup_field = 'client_id'

    def get_queryset(self):
        queryset = Wishlist.objects.select_related('client', 'product_item', 'product_item__product').all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        client_id = self.kwargs['client_id']
        try:
            client = Client.objects.get(pk=client_id)
            Wishlist.objects.filter(client_id=client.pk).delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except (TypeError, ValueError, ValidationError, Client.DoesNotExist):
            raise Http404
