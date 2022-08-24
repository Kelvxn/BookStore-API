from django.contrib import admin

from .models import Author, Book, Publisher


# Register your models here.
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):

    list_display = ("name", "email", "website")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'email')
    ordering = ('first_name',)
    prepopulated_fields = {"slug": ("first_name", "last_name")}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ("title", "publishers", "page_count")
    list_filter = ("publishers", "authors")
    search_fields = ("authors", "publishers")
