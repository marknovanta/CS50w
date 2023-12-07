from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="watchlist", blank=True)


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    category = models.CharField(max_length=140)
    image = models.URLField(null=True, blank=True)
    description = models.TextField()
    starting_bid = models.FloatField()
    status = models.CharField(max_length=64, default="open")
    winner = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.amount} for {self.listing}, by {self.user}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.content} - {self.user}"
