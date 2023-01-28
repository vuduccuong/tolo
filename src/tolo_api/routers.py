from django.urls import path, include

urlpatterns = [
    path("v1/", include("tolo_account.urls")),
    path("v1/", include("tolo_post.urls")),
]
