# from django.contrib.auth import get_user_model
# from rest_framework import authentication
# from rest_framework import exceptions
#
#
# class CustomAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         username = request.META.get('HTTP_X_USERNAME')
#         if not username:
#             return None
#
#         try:
#             user = get_user_model().objects.get(username=username)
#         except get_user_model().DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user')
#
#         return (user, None)