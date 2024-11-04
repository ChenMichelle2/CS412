# mini_fb/views.py
from django.shortcuts import render
from django.urls import reverse

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
  def get_absolute_url(self):
    '''Return the URL to redirect to after successfully submitting the form.'''
    return reverse('show_profile', args=[str(self.object.pk)])
  
class CreateStatusMessageView(LoginRequiredMixin,CreateView):
  model = StatusMessage
  form_class = CreateStatusMessageForm
  template_name = 'mini_fb/create_status_form.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile = Profile.objects.get(pk=self.kwargs['pk'])
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
    # Redirect to the profile's detail page after posting the status
    return reverse('show_profile', args=[self.kwargs['pk']])
  
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
  def dispatch(self, request, *args, **kwargs):
    pk = self.kwargs.get('pk')
    other_pk = self.kwargs.get('other_pk')
        
    profile = get_object_or_404(Profile, pk=pk)
    other_profile = get_object_or_404(Profile, pk=other_pk)

    # Check for self-friending
    if profile == other_profile:
      print("Cannot add self as a friend.")
    else:
      # Add friend only if it doesn't already exist
      if profile.add_friend(other_profile):
        print("Friendship created successfully.")
      else:
        print("Friendship already exists.")

      # Redirect back to the profile page
      return redirect(reverse('show_profile', kwargs={'pk': pk})) 
    def get_login_url(self) -> str:
      '''Return the URL to the login page.'''
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
class ShowNewsFeedView(LoginRequiredMixin,DetailView):
  """Displays the news feed for a single profile."""
  model = Profile
  template_name = 'mini_fb/news_feed.html'
  context_object_name = 'profile'
  def get_login_url(self) -> str:
    '''Return the URL to the login page.'''
    return reverse('login')
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile = self.get_object()
    context['news_feed'] = profile.get_news_feed()
    return context
    