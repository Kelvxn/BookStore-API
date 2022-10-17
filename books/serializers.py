from rest_framework import serializers

from .models import Author, Book, Publisher, Review


# Serializers
class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    books_published = serializers.StringRelatedField(many=True, read_only=True)
    subscribers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ["url", "name", "email", "website", "subscribers", "books_published"]
        extra_kwargs = {
            "url": { "lookup_field": "slug"},
            "books_published": { "required": False},
            "subscribers": { "required": False},
        }


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    full_name = serializers.ReadOnlyField(source="get_full_name")
    books_written = serializers.HyperlinkedRelatedField(
        view_name="book-detail", many=True, read_only=True
    )

    class Meta:
        model = Author
        fields = [
            "url",
            "full_name",
            "first_name",
            "last_name",
            "email",
            "books_written",
        ]
        extra_kwargs = {
            "url": {"lookup_field": "slug"},
            "books_writtern": {"required": False},
        }


class BookSerializer(serializers.HyperlinkedModelSerializer):

    authors = serializers.StringRelatedField(many=True, read_only=True)
    bookmarks = serializers.SerializerMethodField()
    publisher = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = [
            "url",
            "title",
            "summary",
            "authors",
            "publisher",
            "isbn",
            "page_count",
            "price",
            "purchase_link",
            "date_published",
            "bookmarks"
        ]

    def get_bookmarks(self, obj):
        count = 0
        for i in obj.bookmark.all():
            count += 1
        return count

    def to_internal_value(self, data):
        return data

    def create(self, validated_data):
        publisher = validated_data.pop("publisher")
        p, created = Publisher.objects.get_or_create(name=publisher)
        book = Book.objects.create(publisher=p, **validated_data)
        return book


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        exclude = ["id"]


class BookInstanceSerializer(BookSerializer):

    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Book
        fields = BookSerializer.Meta.fields + ["reviews"]
