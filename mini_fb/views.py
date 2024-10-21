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
  

