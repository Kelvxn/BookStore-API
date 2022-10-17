from rest_framework import exceptions, status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from books.utils import validate_review

from .models import Author, Book, Publisher, Review
from .serializers import AuthorSerializer, BookInstanceSerializer, BookSerializer, PublisherSerializer, ReviewSerializer


# Create your views here.
class APIRoot(APIView):

    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        return Response(
            {
                "Books List": reverse("book-list", request=request, format=format),
                "Authors List": reverse("author-list", request=request, format=format),
                "Publishers List": reverse("publisher-list", request=request, format=format)
            }
        )


class BookViewSet(ModelViewSet):

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    lookup_field = "pk"
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "add_to_bookmark":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permissions() for permissions in permission_classes]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BookInstanceSerializer
        return super().get_serializer_class()

    @action(methods=["post"], detail=True, url_path="bookmark")
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
    
    @action(methods=["post"], detail=True, url_path="review")
    def add_review(self, request, pk=None):
        book = self.get_object()
        data = request.data.get("review")
        cleaned_data = validate_review(data)
        review = Review.objects.create(book=book, user=request.user, review=cleaned_data)
        book.reviews.add(review)
        serializer = BookInstanceSerializer(book, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

 
class AuthorViewSet(ModelViewSet):

    authentication_classes = [BasicAuthentication]
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


class PublisherViewSet(ModelViewSet):

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    lookup_field = "slug"
    queryset = Publisher.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = PublisherSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "subscribe_to_publisher":
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=["post"], detail=True, url_path="subscribe")
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
