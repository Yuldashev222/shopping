from rest_framework import (
    viewsets,
    permissions,
    response,
    status,
    exceptions,
    mixins
)

from api.v1.products.models import Brand
from api.v1.products.serializers.brands import ProductBrandSerializer, ProductBrandDashboardSerializer
from api.v1.accounts.permissions import IsStaff


class ProductBrandAPIViewSet(mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = ProductBrandSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return []
        return [permission() for permission in [permissions.IsAuthenticated & IsStaff]]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            if len(request.data) > 20:
                raise exceptions.ValidationError('you can send a maximum of 20 objects')
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductBrandDashboardAPIViewSet(mixins.RetrieveModelMixin, ProductBrandAPIViewSet):
    serializer_class = ProductBrandDashboardSerializer

    def get_permissions(self):
        return [permission() for permission in [permissions.IsAuthenticated & IsStaff]]

    def get_queryset(self):
        queryset = Brand.objects.select_related('creator').all()
        return queryset
