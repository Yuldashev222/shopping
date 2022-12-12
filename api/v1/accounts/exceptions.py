from rest_framework.exceptions import APIException
from rest_framework import status


class MultiValueError(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS

