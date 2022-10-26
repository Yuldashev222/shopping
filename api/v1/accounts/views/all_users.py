from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import (
    viewsets,
    status
)

from api.v1.accounts.models import CustomUser
from api.v1.accounts.enums import CustomUserRole
from api.v1.accounts.serializers.all_users import UserSerializer


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def user_logout(request, *args, **kwargs):
    # try:
    #     token = request.auth
    #     refresh_token = AccessToken(token)
    #     return Response(status=status.HTTP_205_RESET_CONTENT)
    # except Exception as e:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


