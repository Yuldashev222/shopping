from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from rest_framework import (
    status
)
from rest_framework.decorators import (
    api_view,
    throttle_classes,
    schema,
    authentication_classes,
    permission_classes
)
from rest_framework.throttling import UserRateThrottle
from rest_framework.schemas import AutoSchema

from api.v1.accounts.models import CustomUser
from api.v1.accounts.serializers.passwords import ForgotPasswordSerializer, ResetPasswordSerializer


# class OncePerDayUserThrottle(UserRateThrottle):
#     rate = '3/day'


@api_view(['POST'])
@schema(AutoSchema)
# @throttle_classes([OncePerDayUserThrottle])
@permission_classes([])
def forgot_password(request, *args, **kwargs):
    serializer = ForgotPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    is_success = serializer.save()
    message = {'message': 'A link to reset your password has been sent to your email.'}
    message_status = status.HTTP_200_OK
    if not is_success:
        message = {'message': 'Oops! Something went wrong, please try again later.'}
        message_status = status.HTTP_409_CONFLICT
    return Response(message, status=message_status)


@api_view(['POST'])
@schema(AutoSchema)
@permission_classes([])
# @throttle_classes([OncePerDayUserThrottle])
def reset_password(request, *args, **kwargs):
    token = kwargs.get('token')
    uid = kwargs.get('uidb64')
    try:
        get_id = urlsafe_base64_decode(uid).decode()
        user = CustomUser.objects.get(id=int(get_id))
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    check_token = default_token_generator.check_token(user, token)
    if check_token:
        serializer = ResetPasswordSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Your password has been successfully changed'}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

