from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    status
)
from rest_framework.decorators import (
    api_view,
    throttle_classes,
    schema,
    permission_classes
)
from rest_framework.throttling import UserRateThrottle
from rest_framework.schemas import AutoSchema

from api.v1.accounts.models import CustomUser
from api.v1.accounts.permissions import IsActive
from api.v1.accounts.serializers.passwords import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer
)


class OncePerDayUserThrottle(UserRateThrottle):
    rate = '3/day'


@api_view(['POST'])
@schema(AutoSchema)
@throttle_classes([OncePerDayUserThrottle])
@permission_classes([])
def forgot_password(request, *args, **kwargs):
    serializer = ForgotPasswordSerializer(data=request.data, context={'request': request})
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
def reset_password(request, *args, **kwargs):
    token = request.query_params.get('token')
    uid = request.query_params.get('uid')
    get_id = urlsafe_base64_decode(uid).decode()
    user = get_object_or_404(CustomUser, pk=int(get_id))

    if default_token_generator.check_token(user, token):
        serializer = ResetPasswordSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Your password has been successfully recovered.'}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@schema(AutoSchema)
@permission_classes([IsAuthenticated, IsActive])
def change_password(request, *args, **kwargs):
    serializer = ChangePasswordSerializer(
        data=request.data, instance=request.user, context={'token': request.headers['authorization'].split()[1]}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message': 'Your password has been successfully changed.'}, status=status.HTTP_200_OK)
