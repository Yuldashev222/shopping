from rest_framework import (
    viewsets,
    permissions,
    response,
    status
)

from api.v1.products.models import ProductImage
from api.v1.products.serializers.images import ProductImageSerializer
from api.v1.products.permissions import IsStaffOrReadOnly


class ProductImageAPIViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated & IsStaffOrReadOnly]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
