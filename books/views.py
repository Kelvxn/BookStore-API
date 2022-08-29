from django.http import Http404

from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
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
class APIRoot(GenericAPIView):
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
    permission_classes = (AllowAny,)


class BookDetail(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)

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
        if request.user not in book.bookmark.all():  # type: ignore
            book.bookmark.add(request.user) # type: ignore
            return Response({"Success": "This book has been added to your bookmark"})
        else:
            book.bookmark.remove(request.user) # type: ignore
            return Response(
                {"Success": "This book has been removed from your bookmark"}
            )


class BookCreate(CreateAPIView):

    serializer_class = BookSerializer
    permission_classes = (AllowAny,)


class BookUpdate(RetrieveUpdateAPIView, GenericAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (AllowAny,)


class BookDelete(RetrieveDestroyAPIView, GenericAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminUser,)


class AuthorsList(ListAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(RetrieveAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = "slug"


class PublishersList(ListAPIView):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class PublisherDetail(RetrieveAPIView):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    lookup_field = "slug"


class PublisherCreate(CreateAPIView):

    serializer_class = PublisherSerializer
    permission_classes = (IsAdminUser,)
