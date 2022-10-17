from uuid import uuid4

from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField

from accounts.models import MyUser


# Create your models here.
class Publisher(models.Model):

    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(always_update=True, populate_from="name", unique=True)
    website = models.URLField()
    email = models.EmailField(("Email Address"))
    address = models.CharField(max_length=100, blank=True)
    subscribers = models.ManyToManyField(MyUser, related_name="watching", blank=True)

    # TODO: Use celery to send emails to subscribers when a publisher releases a book.

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("publisher-detail", kwargs={"slug": self.slug})


class Author(models.Model):

    first_name = models.CharField(("First Name"), max_length=30)
    last_name = models.CharField(("Last Name"), max_length=30)
    slug = AutoSlugField(always_update=True, populate_from="get_full_name", unique=True)
    email = models.EmailField(("Email address"))
    subscribers = models.ManyToManyField(MyUser, related_name="subscribed_to", blank=True)

    def __str__(self):
        full_name = self.get_full_name()
        return full_name

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"unique": "A book with this title already exists."},
    )
    summary = models.TextField()
    authors = models.ManyToManyField(Author, related_name="books_written")
    publisher = models.ForeignKey(
        Publisher,
        related_name="books_published",
        on_delete=models.CASCADE,
    )
    date_published = models.DateField()
    isbn = models.CharField(
        ("ISBN"),
        max_length=13,
        unique=True,
        error_messages={
            "unique": "A book with this ISBN already exists",
        }
    )
    page_count = models.PositiveIntegerField(("Number of pages"))
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    purchase_link = models.URLField()

    class Meta:
        ordering = ["-date_published"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.id})


class Review(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    review = models.TextField(help_text="Your review of this book")
    date_posted = models.DateTimeField(auto_now_add=True)
