from rest_framework import viewsets
from rest_framework.response import Response

from tolo_core.logging.app_log import AppLog


# Create your views here.
class AccountViewSet(viewsets.ViewSet):
    def list(self, request):
        AppLog.log_warning()
        return Response(status=200)
