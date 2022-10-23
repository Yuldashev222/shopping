from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import password_validation
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from api.v1.accounts.models import CustomUser


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    forgot_type = serializers.ChoiceField(['email', 'sms'])

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with such email address is not registered')
        return value

    def save(self, **kwargs):
        forgot_type = self.data['forgot_type']
        email = self.data['email']
        user = CustomUser.objects.get(email=email)
        if forgot_type == 'email':
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)
            subject = 'Link to reset your password'
            recipient_list = [settings.EMAIL_HOST_USER]
            message = f'Hi {user}.\n' \
                      'Click the link below to create a new password\n' \
                      f'Link: http://127.0.0.1:8000/api/v1/accounts/reset-password/{uid}/{token}/'
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=recipient_list,
                    fail_silently=True
                )
                return True
            except:
                return False
        return False


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, validators=[password_validation.validate_password])
    re_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({'re_password': ['passwords are not the same']})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        return instance
