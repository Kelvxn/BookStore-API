from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class MyUser(AbstractUser):

    slug = models.SlugField()
    bookmark = models.ManyToManyField("books.Book", related_name="bookmark")

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return full_name
        return self.username

    def save(self,*args, **kwargs):
        if not self.slug:
            full_name = self.get_full_name()
            self.slug = slugify(full_name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"slug": self.slug})
    