# mini_fb/views.py
from django.shortcuts import render
from django.urls import reverse
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from typing import Any

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import *
from .models import *
from .forms import *
import random
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW

# class-based view
class ShowAllProfilesView(ListView):
  '''the view to show all Profiles'''
  model = Profile #the model to display
  template_name = 'mini_fb/show_all_profiles.html'
  context_object_name = 'Profiles' # how to find the data in the template file
  def get_context_data(self, **kwargs):
        # Get the default context data from the ListView
        context = super().get_context_data(**kwargs)

        # Add the logged-in user's profile to the context if they're authenticated
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            context['profile'] = user_profile

        return context

class ShowProfilePageView(DetailView):
  '''shows the profile of one Profile '''
  model = Profile #the model to display
  template_name = 'mini_fb/show_profile.html'
  context_object_name = 'Profile' #how to find the data in the template file

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)    
    profile = self.get_object()
    context['friends'] = profile.get_friends()  # Call the get_friends method from Profile model
    return context

class CreateProfileView(CreateView):
  model = Profile
  form_class = CreateProfileForm
  template_name = 'mini_fb/create_profile_form.html'
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

  def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            form.instance.user = new_user
            return reverse('show_all_profiles')
        else:
            return self.form_invalid(form)
  def get_absolute_url(self):
    '''Return the URL to redirect to after successfully submitting the form.'''
    return reverse('show_all_profiles')
  
class CreateStatusMessageView(LoginRequiredMixin,CreateView):
  model = StatusMessage
  form_class = CreateStatusMessageForm
  template_name = 'mini_fb/create_status_form.html'

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the logged-in user's profile instead of relying on pk
        profile = get_object_or_404(Profile, user=self.request.user)
        context['profile'] = profile  # Pass profile to the template
        return context  
  
  def get_login_url(self) -> str:
    '''Return the URL to the login page.'''
    return reverse('login')

  def form_valid(self, form):
    profile = Profile.objects.get(pk=self.kwargs['pk'])  # Get the profile instance
    form.instance.profile = profile  # Assign the profile to the status message

    sm = form.save()  # save the status message to database

    files = self.request.FILES.getlist('files') # read the file from the form
 
    for file in files:   # Iterate over each uploaded file and create an Image object
      # Create and save each image object associated with the status message
      image = Image(image_file=file, status_message=sm)
      image.save()

    return super().form_valid(form)

  def get_success_url(self):
        # Redirect to the logged-in user's profile page after posting the status
        profile = get_object_or_404(Profile, user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})

  def get_object(self):
        # Fetch the logged-in user's profile instead of using pk
        return get_object_or_404(Profile, user=self.request.user)
class UpdateProfileView(LoginRequiredMixin, UpdateView):
  '''Updates the Profile from the form'''
  model = Profile
  form_class = UpdateProfileForm
  template_name = 'mini_fb/update_profile_form.html'

  def get_success_url(self):
    # Redirect to the profile's detail page after updating the profile
    return reverse('show_profile', args=[self.object.pk])

  def get_context_data(self, **kwargs):
    # Add any extra context for the template, like the profile object
    context = super().get_context_data(**kwargs)
    context['profile'] = self.object  # Pass the profile to the template
    return context
  
  def get_login_url(self) -> str:
    '''Return the URL to the login page.'''
    return reverse('login')
  
  def get_object(self):
        # Check if a pk is provided in the URL
        pk = self.kwargs.get('pk', None)
        
        if pk:
            # If pk is provided, get the profile associated with that pk
            return get_object_or_404(Profile, pk=pk)
        else:
            # If no pk is provided, return the profile of the logged-in user
            return get_object_or_404(Profile, user=self.request.user)
  
class DeleteStatusMessageView(LoginRequiredMixin,DeleteView):
  '''deletes a status message'''
  model = StatusMessage
  template_name = 'mini_fb/delete_status_form.html'
  context_object_name = 'status_message'

  def get_login_url(self) -> str:
    '''Return the URL to the login page.'''
    return reverse('login')
  def get_success_url(self):
    '''Redirect to the profile page of the user who owns this status message'''
    profile_id = self.object.profile.pk  # Get the profile ID associated with the status message
    return reverse('show_profile', args=[profile_id])
  
class UpdateStatusMessageView(LoginRequiredMixin,UpdateView):
  '''updates a status message'''
  model = StatusMessage
  template_name = 'mini_fb/update_status_form.html'
  form_class = UpdateStatusMessageForm
  context_object_name = 'status_message'

  def get_login_url(self) -> str:
    '''Return the URL to the login page.'''
    return reverse('login')
  def get_success_url(self):
    '''Redirect to the profile page of the user who owns this status message'''
    profile_id = self.object.profile.pk  # Get the profile ID associated with the status message
    return reverse('show_profile', args=[profile_id])

class CreateFriendView(LoginRequiredMixin, View):
  """Adds a friend relationship between two profiles based on URL parameters"""
  def get_object(self):
        """Fetches the logged-in user's profile."""
        return get_object_or_404(Profile, user=self.request.user)

  def post(self, request, other_pk, *args, **kwargs):
        """Handles the POST request to add a friend."""
        # Get the logged-in user's profile
        user_profile = self.get_object()

        # Get the profile of the user to be added as a friend
        other_profile = get_object_or_404(Profile, pk=other_pk)

        # Check for self-friending
        if user_profile == other_profile:
            print("Cannot add yourself as a friend.")
        else:
            # Add the other profile as a friend if not already a friend
            if user_profile.add_friend(other_profile):
                print("Friendship created successfully.")
            else:
                print("Friendship already exists.")

        # Redirect to the logged-in user's news feed or any other desired page
        return redirect(reverse('show_profile', kwargs={'pk': user_profile.pk}))
  def get_login_url(self) -> str:
        """Return the URL to the login page if the user is not authenticated."""
        return reverse('login')
  
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
  """Displays friend suggestions for a single profile."""
  model = Profile
  template_name = 'mini_fb/friend_suggestions.html'
  context_object_name = 'profile'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile = self.get_object()
    context['friend_suggestions'] = profile.get_friend_suggestions()
    return context
  def get_login_url(self) -> str:
    '''Return the URL to the login page.'''
    return reverse('login')
  
  def get_object(self):
    pk = self.kwargs.get('pk', None)
        
    if pk:
      return get_object_or_404(Profile, pk=pk)
    else:
      return get_object_or_404(Profile, user=self.request.user)
class ShowNewsFeedView(LoginRequiredMixin,DetailView):
  """Displays the news feed for a single profile."""
  model = Profile
  template_name = 'mini_fb/news_feed.html'
  context_object_name = 'status_messages'

  def get_login_url(self) -> str:
    '''Return the URL to the login page.'''
    return reverse('login')
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile = self.get_object()
    context['news_feed'] = profile.get_news_feed()
    return context
  def get_object(self):
    pk = self.kwargs.get('pk', None)
        
    if pk:
      return get_object_or_404(Profile, pk=pk)
    else:
      return get_object_or_404(Profile, user=self.request.user)
    
