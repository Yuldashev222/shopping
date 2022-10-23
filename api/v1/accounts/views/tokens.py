from rest_framework_simplejwt import views, exceptions
from rest_framework.response import Response
from rest_framework import status

from api.v1.accounts.serializers.tokens import TokenSerializer


class LoginAPIView(views.TokenObtainPairView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)