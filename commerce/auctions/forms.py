from django import forms
from .models import AuctionListing, Comment, Bid, WatchList


class BidForm(forms.Form):
    amount = forms.IntegerField()
    widgets = {'amount': forms.TextInput(attrs={'class': 'form-control'})}


class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ('item', 'description', 'image_url', 'owner', 'category', 'bid', 'is_closed')
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'owner': forms.HiddenInput(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'comment', 'listing')
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'listing': forms.HiddenInput(attrs={'class': 'form-control'})
        }


class WatchListForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = ('user', 'auctions')
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'auctions': forms.HiddenInput(attrs={'class': 'form-control'})
        }

