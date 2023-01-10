from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tolo_account.url")),
    path("", include("tolo_auth.url")),
]
