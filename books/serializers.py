from rest_framework import serializers

from .models import Author, Book, Publisher


# Serializers
class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="author-detail", 
        read_only=True,
        lookup_field="slug",
    )
    full_name = serializers.ReadOnlyField(source="get_full_name")

    class Meta:
        model = Author
        fields = ["url", "full_name", "email",]


class BookSerializer(serializers.HyperlinkedModelSerializer):

    publishers = serializers.HyperlinkedRelatedField(
        view_name="publisher-detail",
        lookup_field="slug",
        read_only=True
    )
    authors = AuthorSerializer(many=True, read_only=True)
    bookmark = serializers.StringRelatedField( read_only=True, many=True)

    class Meta:
        model = Book
        fields = [
            "url",
            "title",
            "description",
            "authors",
            "publishers",
            "isbn",
            "page_count",
            "date_published",
            "bookmark"
        ]

    def create(self, validated_data):
        return super().create(validated_data)

class PublisherSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="publisher-detail", 
        read_only=True,
        lookup_field="slug",
    )
    subscribers = serializers.StringRelatedField(read_only=True, many=True)
    books = serializers.HyperlinkedRelatedField(
        view_name="book-detail",
        many=True,
        read_only=True
    )

    class Meta:
        model = Publisher
        fields = ["url", "name", "email", "website", "subscribers", "books"]
