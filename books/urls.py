from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import APIRoot, AuthorViewSet, BookViewSet, PublisherViewSet


router = SimpleRouter()
router.register(r'authors', AuthorViewSet, "author")
router.register(r'books', BookViewSet, "book")
router.register(r'publishers', PublisherViewSet, "publisher")

urlpatterns = [
    path("", APIRoot.as_view()),
]

urlpatterns += router.urls
