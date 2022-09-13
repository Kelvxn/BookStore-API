from django.utils.text import slugify

from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Author, Book, Publisher
from .serializers import AuthorSerializer, BookSerializer, PublisherSerializer


# Create your views here.
class APIRoot(APIView):

    def get(self, request, format=None):
        return Response(
            {
                "Books List": reverse("book-list", request=request, format=format),
                "Authors List": reverse("author-list", request=request, format=format),
                "Publishers List": reverse(
                    "publisher-list", request=request, format=format
                ),
            }
        )


class BookViewSet(ModelViewSet):

    authentication_classes = [BasicAuthentication]
    lookup_field = "pk"
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permissions() for permissions in permission_classes]

    @action(methods=["post"], detail=True, url_path="bookmark", permission_classes=[IsAuthenticatedOrReadOnly])
    def add_to_bookmark(self, request, pk=None):
        book = self.get_object()
        if request.user not in book.bookmark.all():
            book.bookmark.add(request.user)
            return Response(
                {"Success": f"{book} has been added to your bookmark."},
                status=status.HTTP_200_OK,
            )
        else:
            book.bookmark.remove(request.user)
            return Response(
                {"Success": f"{book} has been removed from your bookmark."},
                status=status.HTTP_200_OK,
            )


class AuthorViewSet(ModelViewSet):

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    lookup_field = "slug"
    queryset = Author.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        serializer.validated_data["slug"] = slugify(f"{first_name} {last_name}")
        return super().perform_update(serializer)


class PublisherViewSet(ModelViewSet):

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    lookup_field = "slug"
    queryset = Publisher.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = PublisherSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        name = serializer.validated_data["name"]
        serializer.validated_data["slug"] = slugify(name)
        return super().perform_update(serializer)

    @action(methods=["post"], detail=True, url_path="subscribe", permission_classes=[IsAuthenticatedOrReadOnly])
    def subscribe_to_publisher(self, request, slug=None):
        publisher = self.get_object()
        if request.user not in publisher.subscribers.all():
            publisher.subscribers.add(request.user)
            return Response(
                {"Success": f"You are now subscribed to {publisher}."},
                status=status.HTTP_200_OK,
            )
        else:
            publisher.subscribers.remove(request.user)
            return Response(
                {"Success": f"You have unsubscribed from {publisher}."},
                status=status.HTTP_200_OK,
            )
