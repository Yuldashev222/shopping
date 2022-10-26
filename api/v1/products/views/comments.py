from rest_framework import (
    viewsets,
    permissions,
    response,
    status
)

from api.v1.products.models import ProductComment
from api.v1.products.serializers.comments import ProductCommentSerializer
from api.v1.products.permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly


class ProductCommentAPIViewSet(viewsets.ModelViewSet):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [permissions.IsAuthenticated & (IsOwnerOrReadOnly | IsStaffOrReadOnly)]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
