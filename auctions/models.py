from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=64)
    image = models.CharField(max_length=100)
    bid = models.IntegerField()

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()
