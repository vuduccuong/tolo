from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from rest_framework.response import Response

from tolo_account.serializers.user_profile import (
    UserSerializer,
    CreateProfileSerializer,
)
from tolo_auth.serializers.user import CreateUserSerializer
from tolo_core.view_mixin.jwt_view import JwtAuthViewSet

User = get_user_model()


# Create your views here.
class AccountViewSet(JwtAuthViewSet):
    def list(self, request):
        user = request.user
        ft = Q(pk=user.id)
        if user.is_staff or user.is_superuser:
            ft = Q()
        users = User.objects.filter(ft).exclude(Q(is_active=0))
        return Response(
            data={"users": UserSerializer(users, many=True).data}, status=200
        )

    def create(self, request):
        data = request.data.copy()
        user_serializer = CreateUserSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = user_serializer.save()
            profile = dict(
                first_name=data.pop("first_name", ""),
                middle_name=data.pop("middle_name", ""),
                last_name=data.pop("last_name", ""),
                avatar=data.pop("avatar", ""),
                birthday=datetime.utcnow(),
                bio=data.pop("bio", ""),
                user_id=user.id,
            )
            profile_serializer = CreateProfileSerializer(data=profile)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        return Response(data=profile_serializer.data, status=200)
