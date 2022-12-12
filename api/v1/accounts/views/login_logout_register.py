from rest_framework_simplejwt import views, exceptions
from rest_framework import status
from api.v1.accounts.serializers.tokens import TokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from api.v1.accounts.permissions import IsStaff, IsVendor
from api.v1.accounts.serializers.staffs import StaffRegisterSerializer
from api.v1.accounts.serializers.clients import ClientRegisterSerializer


class LoginAPIView(views.TokenObtainPairView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request, *args, **kwargs):
    print(request.headers['authorization'].split()[1])  # last
    return Response(status=HTTP_204_NO_CONTENT)


# 998974068601   asdasdasdasdasd
class ClientRegisterAPIView(CreateAPIView):
    serializer_class = ClientRegisterSerializer
    permission_classes = [~IsAuthenticated | IsStaff]


#  998974068444   123123asdasd  vendor
#  998974068000   123123asdasd  manager
class StaffRegisterAPIView(CreateAPIView):
    serializer_class = StaffRegisterSerializer
    permission_classes = [IsAuthenticated, IsStaff, ~IsVendor]
