from rest_framework import serializers, exceptions
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from api.v1.accounts.services import get_tokens_user


class TokenSerializer(serializers.Serializer):
    token_class = RefreshToken
    username = serializers.CharField()
    password = PasswordField()

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def validate(self, attrs):
        authenticate_kwargs = {
            'username': attrs['username'],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(self.user)
        del attrs['username'], attrs['password']
        attrs["token"] = str(refresh.access_token)
        attrs["user_id"] = self.user.id
        attrs["user_role"] = self.user.role

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return attrs

    @classmethod
    def get_token(cls, user):
        return get_tokens_user(user)
