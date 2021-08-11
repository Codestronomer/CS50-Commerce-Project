from django import forms
from .models import AuctionListing, Comment, Bid


class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ('item', 'owner', 'description', 'image_url', 'category', 'bid', 'is_closed')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'comment', 'active', 'listing')


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('user', 'amount')
