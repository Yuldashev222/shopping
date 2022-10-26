from rest_framework import (
    viewsets,
    permissions,
    response,
    status
)

from api.v1.products.models import ProductStar
from api.v1.products.serializers.stars import ProductStarSerializer
from api.v1.products.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly


class ProductStarAPIViewSet(viewsets.ModelViewSet):
    queryset = ProductStar.objects.all()
    serializer_class = ProductStarSerializer
    permission_classes = [permissions.IsAuthenticated & (IsStaffOrReadOnly | IsOwnerOrReadOnly)]

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
