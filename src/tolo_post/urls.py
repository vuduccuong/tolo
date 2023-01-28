from rest_framework.routers import SimpleRouter

from tolo_post import views

router = SimpleRouter(trailing_slash=False)
router.register("posts", viewset=views.PostViewSet, basename="PostViewSet")

urlpatterns = router.urls
