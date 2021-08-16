from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    item = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_listings', blank=True)
    description = models.TextField()
    image_url = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category_for_listing")
    created = models.DateTimeField(auto_now_add=True)
    bid = models.IntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    bids = models.ManyToManyField('Bid', related_name='bids_in_the_auction', blank=True)
    last_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='last_bid_for_the_auction', blank=True,
                                 null=True)

    def __str__(self):
        return f'{self.item}: {self.bid}'


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid')
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="auction_listing")
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bid of {self.amount} made by {self.user}'


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


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    auctions = models.ManyToManyField(AuctionListing, related_name='auctions_in_the_watchlist', blank=True)

    def __str__(self):
        return f'watchlist for {self.user}'
