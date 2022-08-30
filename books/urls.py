from django.urls import path

from . import views


urlpatterns = [
    path("", views.APIRoot.as_view()),
    path("books/", views.BooksList.as_view(), name="books_list"),
    path("books/<uuid:pk>/", views.BookDetail.as_view(), name="book-detail"),
    path("books/new/", views.BookCreate.as_view(), name="book_create"),
    path("books/<uuid:pk>/update/", views.BookUpdate.as_view(), name="book_update"),
    path("books/<uuid:pk>/delete/", views.BookDelete.as_view(), name="book_delete"),
    path("authors/", views.AuthorsList.as_view(), name="authors_list"),
    path("authors/<slug:slug>/", views.AuthorDetail.as_view(), name="author-detail"),
    path("authors/new/a/", views.AuthorCreate.as_view(), name="author-create"),
    path("authors/<slug:slug>/update/", views.AuthorUpdate.as_view(), name="author-update"),
    path("authors/<slug:slug>/delete/", views.AuthorDelete.as_view(), name="author-delete"),
    path("publishers/", views.PublishersList.as_view(), name="publishers_list"),
    path("publishers/<slug:slug>/", views.PublisherDetail.as_view(), name="publisher-detail"),
    path("publishers/new/p/", views.PublisherCreate.as_view(), name="publisher-create"),
    path("publishers/<slug:slug>/update/", views.PublisherUpdate.as_view(), name="publisher-update"),
    path("publishers/<slug:slug>/delete/", views.PublisherDelete.as_view(), name="publisher-delete"),
]
