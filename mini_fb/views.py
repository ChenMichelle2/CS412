# mini_fb/views.py
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from django.views.generic import *
from .models import *
from .forms import *
import random

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
  
class CreateStatusMessageView(CreateView):
  model = StatusMessage
  form_class = CreateStatusMessageForm
  template_name = 'mini_fb/create_status_form.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    profile = Profile.objects.get(pk=self.kwargs['pk'])
    context['profile'] = profile  # Pass profile to the template
    return context

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
  
class UpdateProfileView(UpdateView):
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
  
class DeleteStatusMessageView(DeleteView):
  '''deletes a status message'''
  model = StatusMessage
  template_name = 'mini_fb/delete_status_form.html'
  context_object_name = 'status_message'
  
  def get_success_url(self):
    '''Redirect to the profile page of the user who owns this status message'''
    profile_id = self.object.profile.pk  # Get the profile ID associated with the status message
    return reverse('show_profile', args=[profile_id])
  
class UpdateStatusMessageView(UpdateView):
  '''updates a status message'''
  model = StatusMessage
  template_name = 'mini_fb/update_status_form.html'
  form_class = UpdateStatusMessageForm
  context_object_name = 'status_message'
  
  def get_success_url(self):
    '''Redirect to the profile page of the user who owns this status message'''
    profile_id = self.object.profile.pk  # Get the profile ID associated with the status message
    return reverse('show_profile', args=[profile_id])

