# blog/views.py
# define the views for the blog app
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from typing import Any

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView ## NEW
from .models import * #imporr the models (e.g. Article)
from .forms import * # impoort the forms (e.g. CreateCommentForm)
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW

import random

# class-based view
class ShowAllView(ListView):
  '''the view to show all articles'''
  model = Article #the model to display
  template_name = 'blog/show_all.html'
  context_object_name = 'articles' # how to find the data in the template file

  def dispatch(self, *args, **kwargs):
    '''implement this methos to add some debug tracing'''
    print(f"ShowAllView.dispatch; self.request.user={self.request.user}")
    return super().dispatch(*args, **kwargs)

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
  
class CreateArticleView(LoginRequiredMixin,CreateView):
  '''A view class to create a new Article instance'''

  form_class = CreateArticleForm
  template_name = 'blog/create_article_form.html'
  model = Article ## add this model and the QuerySet will automatically find instance by PK
  context_object_name = "article"

  def get_login_url(self) -> str:
    '''Return the URL to the login page.'''
    return reverse('login')
  
  def form_valid(self, form):
    '''Handle the form submission to create a new Article object.'''
    print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')
    return super().form_valid(form)

class RegistrationView(CreateView):
    ''' show/process form for account registration '''
    template_name = 'blog/register.html'
    form_class = UserCreationForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
      '''Handle the User Creation form submission'''
      # if we recieved  a HTTP POST, we handle:
      if self.request.POST:
        print(f"RegistrationView.dispatch: self.request.POST = {self.request.POST}")

        #reconstruct the UserCreationForm from the POST data
        form = UserCreationForm(self.request.POST)

        if not form.is_valid():
          print(f"form.errors={form.errors}")

          #let CreateView.dispatch handle the problem
          return super().dispatch(request, *args, **kwargs)
        
        # create the user and login
        user = form.save()     
        print(f"RegistrationView.form_valid(): Created user= {user}")   

        login(self.request, user)
        print(f"RegistrationView.form_valid(): User is logged in")   

        #return a response
        return redirect(reverse('show_all_blog'))
      #let CreateView.dispatch handle the HTTP GET request
      return super().dispatch(request, *args, **kwargs)

