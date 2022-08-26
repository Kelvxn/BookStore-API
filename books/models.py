from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import MyUser


# Create your models here.
class Publisher(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    website = models.URLField()
    email = models.EmailField(("Email Address"), max_length=254, unique=True)
    address = models.CharField(max_length=100)
    subscribers = models.ManyToManyField(MyUser, related_name="subscribers", blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("publisher-detail", kwargs={"slug": self.slug})


class Author(models.Model):

    first_name = models.CharField(("First Name"), max_length=30)
    last_name = models.CharField(("Last Name"), max_length=30)
    slug = models.SlugField(max_length=100)
    email = models.EmailField(("Email address"), unique=True)
    about = models.TextField(max_length=250)

    def __str__(self):
        return f"{self.first_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = self.get_full_name()
            self.slug = slugify(full_name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"unique": "A book with this title already exists."}
    )
    description = models.TextField()
    authors = models.ManyToManyField(Author, related_name="authors")
    publisher = models.ForeignKey(
        Publisher, related_name="books_published", on_delete=models.CASCADE, null=True, blank=True
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

    class Meta:
        ordering = ("-date_published",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.id})
