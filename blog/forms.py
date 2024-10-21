# blog/form.py

from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
  '''A form to add a Comment on an Article to the Database'''

  class Meta:
    '''associate this HTML form with the Comment data model'''
    model = Comment
    fields = ['article', 'author', 'text']

class CreateArticleForm(forms.ModelForm):
  '''A form to add a new Article to the Database'''

  class Meta:
    '''Associate this HTML form with the Article data model'''
    model = Article
    fields = ['author', 'title', 'text', 'image_file']