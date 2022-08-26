from rest_framework import serializers

from .models import Author, Book, Publisher


# Serializers
class PublisherSerializer(serializers.ModelSerializer):

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="publisher-detail", 
    #     read_only=True,
    #     lookup_field="slug",
    # )
    books_published = serializers.HyperlinkedRelatedField(
        view_name="book-detail",
        many=True,
        read_only=True,
        required=False
    )
    subscribers = serializers.StringRelatedField(read_only=True, many=True, required=False)

    class Meta:
        model = Publisher
        fields = ["id", "name", "email", "website", "subscribers", "books_published"]

        
class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    full_name = serializers.ReadOnlyField(source="get_full_name")

    class Meta:
        model = Author
        fields = ["url", "full_name", "first_name", "last_name", "email"]
        extra_kwargs = {
            "url": {"view_name": "author-detail", "lookup_field": "slug"},
            "email": {"required": False}
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
            "bookmarked_by"
        ]
        # extra_kwargs = {
        #     "publisher": {"view_name": "publisher-detail"}
        # }

    def get_bookmarked_by(self, obj):
        count = 0
        for users in obj.bookmark.all():
            count += 1
        return count

    def create(self, validated_data):
        publisher = validated_data.pop("publisher")
        # # authors = validated_data.pop("authors")
        # author_obj = {}
        # for i in authors:
        #     author_obj = dict(i)
        # a = Author.objects.filter(**author_obj).exists()
        # if not a:
        #     a = Author.objects.create(**author_obj)
        # else:
        #     a = Author.objects.get(**author_obj)

        p = Publisher.objects.filter(**publisher).exists()
        if p:
            p = Publisher.objects.get(**publisher)
        else:
            p = Publisher.objects.create(**publisher)
            
        book = Book.objects.create(publisher=p,  **validated_data)
        return book

