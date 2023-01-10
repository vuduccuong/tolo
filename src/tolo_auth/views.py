from django.contrib.auth import authenticate, login
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tolo_auth.serializers.auth import AuthSerializer
from tolo_core.constants.http_method import HttpMethod
from tolo_core.helpers.jwt_token import JwtHelper


# Create your views here.
class AuthViewSet(viewsets.ViewSet):
    authentication_classes = ()
    serializer_class = AuthSerializer

    @action(methods=[HttpMethod.POST], detail=False)
    def login(self, request):
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = authenticate(request, **validated_data)
        if user is not None:
            login(request, user)
            setattr(request, "user", user)
            payload = dict(uid=user.id, email=user.email, role=1)
            jwt = JwtHelper().endcode_token(payload)
            return Response(
                data={"access_token": jwt, "token_type": "Bearer"},
                status=status.HTTP_200_OK,
            )

        return Response(status == status.HTTP_401_UNAUTHORIZED)
