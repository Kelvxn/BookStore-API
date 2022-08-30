from django.urls import path

from .views import (
    APIRoot,
    AuthorCreate,
    AuthorDelete,
    AuthorDetail,
    AuthorUpdate,
    AuthorsList,
    BookCreate,
    BookDelete,
    BookDetail,
    BookUpdate,
    BooksList,
    PublisherCreate,
    PublisherDelete,
    PublisherDetail,
    PublisherUpdate,
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
    path("authors/new/a/", AuthorCreate.as_view(), name="author-create"),
    path("authors/<slug:slug>/update/", AuthorUpdate.as_view(), name="author-update"),
    path("authors/<slug:slug>/delete/", AuthorDelete.as_view(), name="author-delete"),
    path("publishers/", PublishersList.as_view(), name="publishers_list"),
    path("publishers/<slug:slug>/", PublisherDetail.as_view(), name="publisher-detail"),
    path("publishers/new/p/", PublisherCreate.as_view(), name="publisher-create"),
    path("publishers/<slug:slug>/update/", PublisherUpdate.as_view(), name="publisher-update"),
    path("publishers/<slug:slug>/delete/", PublisherDelete.as_view(), name="publisher-delete"),
]
