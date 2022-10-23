from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import (
    status,
    mixins,
    generics,
    viewsets,
)

from api.v1.accounts.models import Client
from api.v1.accounts.serializers.clients import ClientSerializer


class ClientAPIView(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def list(self, request, *args, **kwargs):
        return super(ClientAPIView, self).list(request, *args, **kwargs)
