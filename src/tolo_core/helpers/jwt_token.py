import jwt
from django.conf import settings

from tolo_core.exceptions.token_expired import TokenExpired, TokenInvalid


class JwtHelper:
    ALGORITHM = "HS256"

    @staticmethod
    def get_secret():
        return settings.SECRET_KEY

    def endcode_token(self, payload):
        return jwt.encode(payload, self.get_secret(), algorithm=self.ALGORITHM)

    def decode_token(self, token):
        try:
            return jwt.decode(token, self.get_secret(), algorithms=[self.ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise TokenExpired()
        except jwt.DecodeError:
            raise TokenInvalid()
