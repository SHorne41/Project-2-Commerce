from django import forms
from .models import Listing, Bid

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
        fields = ['bidAmount', 'user']
        widgets = {
            'user': forms.HiddenInput()
        }
