from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from autoslug import AutoSlugField
from rest_framework.authtoken.models import Token


# Create your models here.
class MyUser(AbstractUser):

    slug = AutoSlugField(populate_from="get_full_name", unique=True)
    bookmark = models.ManyToManyField("books.Book", related_name="bookmark", blank=True)

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return full_name
        return self.username
 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
