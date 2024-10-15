# blog/form.py

from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
  '''A form to add a Comment on an Article to the Database'''

  class Meta:
    '''associate this HTML form with the Comment data model'''
    model = Comment
    fields = ['article', 'author', 'text']