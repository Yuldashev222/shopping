from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.db.models import Q
from django.conf import settings

UserModel = get_user_model()


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, phone_number=None, password=None, **kwargs):
        if not username:
            username = email or phone_number
        if username is None or password is None:
            return
        user = UserModel.objects.filter(Q(phone_number=username) | Q(email=username)).first()
        if not user:
            login_valid = bool(username in [settings.BASE_USER_EMAIL, settings.BASE_USER_PHONE_NUMBER])
            password_valid = check_password(password, settings.BASE_USER_PASSWORD)
            if login_valid and password_valid:
                user = UserModel.objects.create_superuser(
                    first_name='super',
                    last_name='user',
                    email=settings.BASE_USER_EMAIL,
                    phone_number=settings.BASE_USER_PHONE_NUMBER,
                    password=password
                )
                return user
            else:
                UserModel().set_password(password)
                return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
