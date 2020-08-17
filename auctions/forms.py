from django import forms
from .models import Listing, Bid, Comment, Watchlist

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'image', 'currentBid', 'owner']
        widgets = {
            'owner': forms.HiddenInput()
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bidAmount', 'user', 'listing']
        widgets = {
            'user': forms.HiddenInput(),
            'listing': forms.HiddenInput()
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'listing', 'comment']
        widgets = {
            'user': forms.HiddenInput(),
            'listing': forms.HiddenInput(),
        }
        labels = {
            'comment': ''
        }

class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['user', 'listing']
        widgets = {
            'user': forms.HiddenInput(),
            'listing': forms.HiddenInput()
        }
