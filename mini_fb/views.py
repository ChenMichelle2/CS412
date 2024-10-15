# mini_fb/views.py
from django.shortcuts import render

# Create your views here.
from django.views.generic import *
from .models import *

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