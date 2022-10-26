from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    settings,
    mixins,
    response,
    status,
)

from api.v1.accounts.models import Vendor
from api.v1.accounts.serializers.vendors import CreateVendorSerializer
from api.v1.accounts.permissions import IsLeader


@api_view(['POST'])
@permission_classes([IsAuthenticated & IsLeader])
def vendor_register(request, *args, **kwargs):
    serializer = CreateVendorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return response.Response(serializer.data, status=status.HTTP_201_CREATED)
