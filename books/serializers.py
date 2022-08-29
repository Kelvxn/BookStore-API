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
            "url": {"view_name": "publisher-detail", "lookup_field": "slug"}
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
            "description",
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
        authors = validated_data.pop("authors")
        authors = json.loads(json.dumps(authors))
        author_objs = []
        a = None 
        for author in authors:
            fn = ln = email = ""
            for i in author.values():
                fn, ln, email = author.values()
                a = Author.objects.filter(first_name=fn, last_name=ln, email=email).exists()
                if not a:
                    a = Author.objects.create(first_name=fn, last_name=ln, email=email)
                else:
                    a = Author.objects.get(first_name=fn, last_name=ln, email=email)
            author_objs.append(a)
        publisher = validated_data.pop("publisher")
        p = Publisher.objects.filter(**publisher).exists()
        if not p:
            p = Publisher.objects.create(**publisher)
        else:
            p = Publisher.objects.get(**publisher)
        book = Book.objects.create(publisher=p, **validated_data)
        for i in author_objs:
            book.authors.add(i)
        return book
