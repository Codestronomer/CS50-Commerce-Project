from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid')
    amount = models.FloatField()

    def __str__(self):
        return f'Bid of {self.amount} made by {self.user}'


class AuctionListing(models.Model):
    item = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_listings', blank=True)
    description = models.TextField()
    image_url = models.CharField(max_length=300)
    category = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name='watch_listings')
    starting_bid = models.FloatField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item}: {self.bid}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('created_on',)

    def __str__(self):
        return f'comment by {self.user} on {self.listing}'
