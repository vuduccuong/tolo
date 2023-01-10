from django.contrib.auth import get_user_model
from rest_framework import serializers

from tolo_core.exceptions.token_expired import TokenInvalid

User = get_user_model()


class JwtPayloadSerizlizer(serializers.Serializer):
    uid = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.IntegerField(required=False)

    def validate(self, attrs):
        try:
            user = User.objects.get(pk=attrs.get("uid", 0))
        except User.DoesNotExist:
            raise TokenInvalid()

        if user.email != attrs.get("email", ""):
            raise TokenInvalid()

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """
        Do not implement
        """
        raise NotImplementedError

    def update(self, instance, validated_data):
        """
        Do not implement
        """
        raise NotImplementedError
