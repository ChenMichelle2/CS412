from django import forms
from .models import Profile, Wishlist

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