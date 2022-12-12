from rest_framework import serializers
from rest_framework.exceptions import NotFound
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import password_validation
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from api.v1.accounts.models import CustomUser


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    forgot_type = serializers.ChoiceField(['email', 'sms'])

    def validate_email(self, value):
        user = get_object_or_404(CustomUser, email=value)
        if not user.active_object():
            raise NotFound()
        return value

    def save(self, **kwargs):
        forgot_type = self.data['forgot_type']
        email = self.data['email']
        user = CustomUser.objects.get(email=email)
        if forgot_type == 'email':
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)
            subject = 'Link to reset your password'
            current_site = get_current_site(self.context['request']).domain
            url = f'http://{current_site}{reverse("reset-password")}?uid={uid}&token={token}'
            message = f'Hi {user}.\nClick the link below to create a new password\nLink: {url}'

            try:
                user.email_user(subject=subject, message=message, fail_silently=True)
                return True
            except ValueError:
                return False
        return False


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, validators=[password_validation.validate_password])
    re_new_password = serializers.CharField()

    def validate(self, attrs):
        if not self.instance.active_object():
            raise NotFound()
        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError({'re_new_password': ['passwords are not the same']})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField(max_length=128, validators=[password_validation.validate_password])
    re_password = serializers.CharField()

    def validate(self, attrs):
        if not self.instance.check_password(attrs['old_password']):
            raise serializers.ValidationError({'old_password': ['The password was entered incorrectly.']})

        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({'re_password': ['passwords are not the same']})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save() # last
        return instance
