from os import path

from rest_framework.routers import SimpleRouter

from tolo_account import views

router = SimpleRouter(trailing_slash=False)
router.register("accounts", viewset=views.AccountViewSet, basename="AccountViewSet")

urlpatterns = router.urls
