from rest_framework.routers import SimpleRouter

from tolo_auth import views

router = SimpleRouter(trailing_slash=False)
router.register("auth", viewset=views.AuthViewSet, basename="AuthViewSet")

urlpatterns = router.urls
