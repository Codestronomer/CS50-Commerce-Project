from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    slug = models.SlugField()
    image = models.ImageField()
    category = models.CharField(max_length=250)
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)


class Bids(models.Model):
    pass


class Comment(models.Model):
    pass