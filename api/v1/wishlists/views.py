from rest_framework import (
    viewsets,
    mixins,
    status,
    response,
    permissions as rest_permissions
)

from api.v1.general.permissions import IsStaff, IsClient, IsOwnerClient
from .models import Wishlist
from .serializers import WishlistSerializer, WishlistListRetrieveSerializer


class WishlistModelViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [rest_permissions.IsAuthenticated, IsClient, IsOwnerClient]

    def get_queryset(self):
        queryset = Wishlist.objects.filter(client_id=self.request.user.id).select_related('product').all()
        return queryset

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            Wishlist.objects.bulk_create()

            if len(request.data) > 20:
                return response.Response(
                    {'detail': ['You must send a maximum of 20 objects!']}, status=status.HTTP_207_MULTI_STATUS
                )

            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WishlistListRetrieveAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = WishlistListRetrieveSerializer
    permission_classes = [rest_permissions.IsAuthenticated, IsStaff]

    def get_queryset(self):
        queryset = Wishlist.objects.select_related('product').all()
        return queryset
