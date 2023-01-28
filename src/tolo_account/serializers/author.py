from django.contrib.auth import get_user_model
from rest_framework import serializers

from tolo_account.serializers.user_profile import UserProfileSerializer


class AuthorSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "userprofile",
        ]
