from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'image_url']

class AddWishlist(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['dragon', 'parent_1', 'parent_2']
        widgets = {
            'dragon': forms.Select(attrs={'class': 'form-control'}),
            'parent_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Parent 1'}),
            'parent_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Parent 2'}),
        }

class AddFav(forms.ModelForm):
    class Meta:
        model = FavoriteDragon
        fields = ['dragon']
        widgets = {
            'dragon': forms.Select(attrs={'class': 'form-control'})
        }

class RemoveFromWishlistForm(forms.Form):
    dragon = forms.ModelChoiceField(
        queryset=Dragon.objects.none(),
        label="Select a dragon to remove",
        empty_label="(Select a dragon)"
    )

class UpdateProfileDragonForm(forms.ModelForm):
  '''a form that updates a Profile'''
  class Meta:
    model = Profile
    fields = ['image_url']