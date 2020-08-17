from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=64)
    image = models.CharField(max_length=100)
    currentBid = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    open = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.title}, Current bid: {self.currentBid}"

class Watchlist(models.Model):
    listing = models.ManyToManyField(Listing)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()

class Bid(models.Model):
    bidAmount = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE)
