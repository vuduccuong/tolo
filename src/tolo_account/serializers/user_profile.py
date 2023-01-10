from django.contrib.auth import get_user_model
from rest_framework import serializers

from tolo_account.models.user_profile import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "avatar",
            "birthday",
            "bio",
        ]


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "last_login",
            "is_superuser",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "userprofile",
        ]


class CreateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=100)
    middle_name = serializers.CharField(required=False, max_length=100)
    last_name = serializers.CharField(required=False, max_length=100, allow_blank=False)
    avatar = serializers.CharField(required=False, max_length=1000, allow_blank=True)
    birthday = serializers.DateTimeField(required=False, allow_null=True, default=None)
    bio = serializers.CharField(
        required=False, allow_null=True, default="", allow_blank=True
    )
    user_id = serializers.IntegerField(required=True)

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        profile = UserProfile()
        for k, v in validated_data.items():
            setattr(profile, k, v)
        profile.save()
        return profile
