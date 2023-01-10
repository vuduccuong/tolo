from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tolo_auth.authentication import JwtAuthentication


class JwtAuthViewSet(viewsets.ViewSet):
    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated,)
