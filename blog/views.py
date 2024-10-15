# blog/views.py
# define the views for the blog app
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView ## NEW
from .models import * #imporr the models (e.g. Article)
from .forms import * # impoort the forms (e.g. CreateCommentForm)
import random

# class-based view
class ShowAllView(ListView):
  '''the view to show all articles'''
  model = Article #the model to display
  template_name = 'blog/show_all.html'
  context_object_name = 'articles' # how to find the data in the template file

class RandomArticleView(DetailView):
  '''Display one Article selected at Random'''
  model = Article
  template_name = 'blog/article.html'
  context_object_name = 'article'

  # AttributeError: Generic detail view RandomArticleView must be called with either
  # one solution: implement get_object method
  def get_object(self):
    '''return one article chosen at random'''
    
    # retrieve all of the article
    all_articles = Article.objects.all()
    # pick one at random
    article = random.choice(all_articles)
    return article
  
class ArticleView(DetailView):
  '''Display one Article selected selected by PK'''
  model = Article #the model to display
  template_name = 'blog/article.html'
  context_object_name = 'article'

class CreateCommentView(CreateView):
  '''A view to create a Comment on an Article'''

  form_class = CreateCommentForm
  template_name = "blog/create_comment_form.html"

  def get_success_url(self) -> str:
    '''Return the URl to redirect '''
    # return 'show_all'
    # return reverse('show_all_blog') #look up the URL show_all
    article = Article.objects.get(pk=self.kwargs['pk'])
    return reverse('article', kwargs={'pk':article.pk})
  
  def form_valid(self, form):
    '''This method is called after the form is validated before saving data to the database.'''

    print(f'CreateCommentView.form_valid(): form ={form.cleaned_data}')
    print(f'CreateCommonView.form_valid(): self.kwargs={self.kwargs}')

    #find the article indentified by e PK from the URL patern
    article = Article.objects.get(pk=self.kwargs['pk'])

    #attach this article to the instance of the comment to ser its FK
    form.instance.article = article #like: comment.article = article

    #delegate work to the superclass version of this method
    return super().form_valid(form)