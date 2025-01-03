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

class UpdateProfileForm(forms.ModelForm):
  '''a form that updates a Profile'''
  class Meta:
    model = Profile
    fields = ['city', 'email','image_url']

class UpdateStatusMessageForm(forms.ModelForm):
    '''form that lets the user update the status message'''
    class Meta:
      model = StatusMessage
      fields = ['message']  # Only allow updating the message text
