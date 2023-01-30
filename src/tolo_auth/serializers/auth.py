from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    remember_me = serializers.BooleanField(required=False)
