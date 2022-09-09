from django.http import Http404
from django.utils.text import slugify

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Author, Book, Publisher
from .serializers import AuthorSerializer, BookSerializer, PublisherSerializer


# Create your views here.
class APIRoot(APIView):
    def get(self, request, format=None):
        return Response(
            {
                "Books List": reverse("books_list", request=request, format=format),
                "Authors List": reverse("authors_list", request=request, format=format),
                "Publishers List": reverse("publishers_list", request=request, format=format),
            }
        )


class BooksList(ListAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        seriliazer = BookSerializer(book, context={"request": request})
        return Response(data=seriliazer.data)

    def post(self, request, pk, format=None):
        book = self.get_object(pk)
        if request.user not in book.bookmark.all():
            book.bookmark.add(request.user)
            return Response({"Success": "This book has been added to your bookmark"})
        else:
            book.bookmark.remove(request.user)
            return Response(
                {"Success": "This book has been removed from your bookmark"}
            )


class BookCreate(CreateAPIView):

    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]


class BookUpdate(RetrieveUpdateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]


class BookDelete(RetrieveDestroyAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]


class AuthorsList(ListAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


class AuthorDetail(RetrieveAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = "slug"


class AuthorCreate(CreateAPIView):

    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]


class AuthorUpdate(RetrieveUpdateAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"

    def perform_update(self, serializer):
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        serializer.validated_data["slug"] = slugify(f"{first_name} {last_name}")
        return super().perform_update(serializer)


class AuthorDelete(RetrieveDestroyAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"


class PublishersList(ListAPIView):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class PublisherDetail(RetrieveAPIView):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def post(self, request, *args, **kwargs):
        publisher = self.get_object()
        if request.user not in publisher.subscribers.all():
            publisher.subscribers.add(request.user)
            return Response({"Success": f"You are now subscribed to {publisher}."})
        else:
            publisher.subscribers.remove(request.user)
            return Response(
                {"Success": f"You have unsubscribed from {publisher}."}
            )


class PublisherCreate(CreateAPIView):

    serializer_class = PublisherSerializer
    permission_classes = [IsAdminUser]


class PublisherUpdate(RetrieveUpdateAPIView):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"

    def perform_update(self, serializer):
        name = serializer.validated_data["name"]
        serializer.validated_data["slug"] = slugify(name)
        return super().perform_update(serializer)


class PublisherDelete(RetrieveDestroyAPIView):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"
