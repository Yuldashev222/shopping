from django.db.models import Q, F, Count
from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets,
    mixins,
    status,
    response,
    permissions as rest_permissions
)

from api.v1.general.permissions import IsStaff, IsClient, IsOwnerClient
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistListSerializer


class WishlistModelViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):

    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [rest_permissions.IsAuthenticated, IsClient, IsOwnerClient]

    def get_queryset(self):
        queryset = Wishlist.objects.filter(
            client_id=self.request.user.id
        ).annotate(asdasd=Count('product_item__product__name')).select_related('product_item')
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

    def get_queryset(self):
        queryset = Wishlist.objects.select_related('product_item').select_related('product_item__product').all()
        return queryset

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(Wishlist, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
