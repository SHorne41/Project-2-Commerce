from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()

class Bids(models.Model):
    bid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()
