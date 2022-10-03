from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailPhoneUsernameAuthenticationBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None

    def authenticate(self, request, username, password):
        email_or_phone = username
        try:
            user = get_user_model().objects.get(
                Q(email=email_or_phone) | Q(phone_number=email_or_phone)
            )

        except get_user_model().DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            return None
