from rest_framework import serializers

from tolo_auth.services.user import UserService


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        email = validated_data.get("email", "")
        password = validated_data.get("password")
        username = validated_data.get("username")

        return UserService().create_normal_user(email, username, password)
