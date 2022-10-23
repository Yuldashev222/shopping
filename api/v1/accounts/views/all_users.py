
from rest_framework.response import Response
from rest_framework import (
    viewsets
)

from api.v1.accounts.models import CustomUser
from api.v1.accounts.serializers.all_users import UserSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def list(self, request, *args, **kwargs):

        # send_mail('blablabla', 'blablabla', from_email=None, recipient_list=['oybekyuldashov54@gmail.com'])
        return super(UserAPIViewSet, self).list(request, *args, **kwargs)
