# mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
  """ A form that Creates a Profile """
  class Meta:
    '''Associate the form with Profile model; select fields'''
    model = Profile
    fields = ['first_name', 'last_name', 'city', 'email','image_url'] #which fields from the model being used

class CreateStatusMessageForm(forms.ModelForm):
  '''a form that creates a Status Message'''
  class Meta:
    model = StatusMessage
    fields = ['message']
