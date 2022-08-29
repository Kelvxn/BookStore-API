from django.urls import path

from .views import (
    APIRoot,
    AuthorDetail,
    AuthorsList,
    BookCreate,
    BookDelete,
    BookDetail,
    BookUpdate,
    BooksList,
    PublisherCreate,
    PublisherDetail,
    PublishersList,
)


urlpatterns = [
    path("", APIRoot.as_view()),
    path("books/", BooksList.as_view(), name="books_list"),
    path("books/<uuid:pk>/", BookDetail.as_view(), name="book-detail"),
    path("books/new/", BookCreate.as_view(), name="book_create"),
    path("books/<uuid:pk>/update/", BookUpdate.as_view(), name="book_update"),
    path("books/<uuid:pk>/delete/", BookDelete.as_view(), name="book_delete"),
    path("authors/", AuthorsList.as_view(), name="authors_list"),
    path("authors/<slug:slug>/", AuthorDetail.as_view(), name="author-detail"),
    path("publishers/", PublishersList.as_view(), name="publishers_list"),
    path("publishers/<slug:slug>/", PublisherDetail.as_view(), name="publisher-detail"),
]
