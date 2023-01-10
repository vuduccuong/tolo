from django.utils.functional import SimpleLazyObject
from rest_framework.authentication import TokenAuthentication

from tolo_core.exceptions.token_expired import Unauthorized, TokenInvalid
from tolo_core.helpers.jwt_token import JwtHelper
from tolo_core.serializers.jwt_payload import JwtPayloadSerizlizer


class JwtAuthentication(TokenAuthentication):
    def authenticate(self, request):
        header = SimpleLazyObject(lambda: self.get_token_header(request)).split()
        if len(header) != 2:
            raise TokenInvalid()
        token = header[1]
        if not token:
            raise Unauthorized()
        user = self.get_jwt_user(token)
        setattr(request, "token", token)
        setattr(request, "user", user)
        return user, token

    @staticmethod
    def get_token_header(request):
        return request.META.get("HTTP_AUTHORIZATION", None)

    @staticmethod
    def get_jwt_user(token):
        payload = JwtHelper().decode_token(token)
        serializer = JwtPayloadSerizlizer(data=payload)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        return validated_data.get("user")
