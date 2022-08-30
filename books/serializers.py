import json

from rest_framework import serializers

from .models import Author, Book, Publisher


# Serializers
class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    books_published = serializers.HyperlinkedRelatedField(
        view_name="book-detail", many=True, read_only=True, required=False
    )
    subscribers = serializers.StringRelatedField(
        read_only=True, many=True, required=False
    )

    class Meta:
        model = Publisher
        fields = ["url", "name", "email", "website", "subscribers", "books_published"]
        extra_kwargs = {
            "url": {"view_name": "publisher-detail", "lookup_field": "slug"},
        }


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    full_name = serializers.ReadOnlyField(source="get_full_name")
    books_written = serializers.HyperlinkedRelatedField(
        view_name="book-detail", required=False, many=True, read_only=True
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
            "url": {"view_name": "author-detail", "lookup_field": "slug"},
        }


class BookSerializer(serializers.HyperlinkedModelSerializer):

    authors = AuthorSerializer(many=True, required=False)
    bookmarked_by = serializers.SerializerMethodField()
    publisher = PublisherSerializer()

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
            "date_published",
            "bookmarked_by",
        ]

    def get_bookmarked_by(self, obj):
        count = 0
        for users in obj.bookmark.all():
            count += 1
        return count

    def create(self, validated_data):
        authors_data = validated_data.pop("authors")
        authors = json.loads(json.dumps(authors_data))
        author_objs = []
        for author in authors:
            fn = ln = email = ""
            a = None
            for i in author.values():
                fn, ln, email = author.values()
                a, created = Author.objects.get_or_create(
                    first_name=fn, last_name=ln, email=email
                )
            author_objs.append(a)
        publisher = validated_data.pop("publisher")
        p, created = Publisher.objects.get_or_create(**publisher)
        book = Book.objects.create(publisher=p, **validated_data)
        for obj in author_objs:
            book.authors.add(obj)
        return book

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.summary = validated_data.get("summary", instance.summary)
        instance.date_published = validated_data.get("date_published", instance.date_published)
        instance.isbn = validated_data.get("isbn", instance.isbn)
        instance.page_count = validated_data.get("page_count", instance.page_count)
        instance.save()
        return instance
