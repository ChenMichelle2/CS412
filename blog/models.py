#blog/models.py
# definite the data objects for our applications
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
  '''Encapsulate the idea of one Article by some author.'''

  # data attributes of a Article:
  user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW
  
  #data attributes of an Article:
  title = models.TextField(blank=False)
  author = models.TextField(blank=False)
  text = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)
  # image_url = models.URLField(blank=True)
  image_file = models.ImageField(blank=True) #NEW

  def __str__(self):
    return f'{self.title} by {self.author}'
    
  def get_comments(self):
    '''Rerurn a QuerySet of all Comments on this Article'''

    #use the ORM to retrieve Comments for which FK is this Article
    comments = Comment.objects.filter(article=self)
    return comments
  def get_absolute_url(self):
    '''Return the URL that will display an instance of this object.'''
    return reverse('article',kwargs={'pk':self.pk})


class Comment(models.Model):
  '''
  Encapsulates the idea of a Comment on an Article
  '''

  # model the 1 ro many relationship with Article (foreign key)
  article = models.ForeignKey("Article", on_delete=models.CASCADE)
  author = models.TextField(blank=False)
  text = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)

  def __str__(self):
    '''Return a string representation of this Comment object.'''
    return f'{self.text}'
  