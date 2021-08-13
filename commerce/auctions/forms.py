from django import forms
from .models import AuctionListing, Comment, Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('amount', 'user', 'auction')
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'auction': forms.HiddenInput(attrs={'class': 'form-control'})
        }


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
        fields = ('user', 'comment', 'active', 'listing')


