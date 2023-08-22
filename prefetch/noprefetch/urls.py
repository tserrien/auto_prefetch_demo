from rest_framework import routers

from .views import PostViewSet, AuthorViewSet

app_name = "nopref"

router = routers.SimpleRouter()
router.register("post", PostViewSet, basename="post")
router.register("author", AuthorViewSet, basename="author")
urlpatterns = router.urls
