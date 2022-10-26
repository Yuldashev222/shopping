from rest_framework.decorators import api_view, permission_classes
from rest_framework import (
    viewsets,
    settings,
    mixins,
    response,
    status
)

from api.v1.accounts.models import Client
from api.v1.accounts.serializers.clients import ClientSerializer, CreateClientSerializer


class ClientAPIViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = settings.api_settings.DEFAULT_PERMISSION_CLASSES


@api_view(['POST'])
@permission_classes([])
def client_register(request, *args, **kwargs):
    serializer = CreateClientSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return response.Response(serializer.data, status=status.HTTP_201_CREATED)
