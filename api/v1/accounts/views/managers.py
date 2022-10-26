from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    settings,
    mixins,
    response,
    status,
)

from api.v1.accounts.models import Manager
from api.v1.accounts.serializers.managers import CreateManagerSerializer
from api.v1.accounts.permissions import IsDirector


@api_view(['POST'])
@permission_classes([IsAuthenticated & IsDirector])
def manager_register(request, *args, **kwargs):
    serializer = CreateManagerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return response.Response(serializer.data, status=status.HTTP_201_CREATED)
