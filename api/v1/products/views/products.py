from rest_framework import (
    viewsets,
    permissions,
    response,
    status
)

from api.v1.products.models import Product
from api.v1.products.serializers.products import ProductSerializer
from api.v1.general.permissions import IsStaff


class ProductAPIViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated, IsStaff]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()
