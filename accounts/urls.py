from rest_framework.routers import SimpleRouter

from .views import UserViewset


router = SimpleRouter()
router.register(r'', UserViewset, basename='user')
urlpatterns = router.urls
