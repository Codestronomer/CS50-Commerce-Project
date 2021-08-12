from django import forms
from .models import AuctionListing, Comment, Bid


class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ('item', 'description', 'image_url', 'category', 'starting_bid', 'is_closed')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'comment', 'active', 'listing')


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('user', 'amount')
