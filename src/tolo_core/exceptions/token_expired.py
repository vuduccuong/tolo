from rest_framework import status
from rest_framework.exceptions import APIException


class TokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Token expired"
    default_code = "001"


class TokenInvalid(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Unauthorized"
    default_code = "002"


class Unauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Unauthorized"
    default_code = "003"
