from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.db.models.query import QuerySet
from typing import Any

# Create your views here.
## formdata.urls.py
## define the URLs for this app

class ShowVoters(ListView):
  model= Voter
  template_name = 'voter_analytics/voters.html'
  context_object_name = 'voters'
def get_queryset(self) -> QuerySet[Any]:
        '''Limit the results to a small number of records'''

        # default query set is all of the records:
        qs = super().get_queryset()
        # return qs[:25] # limit to 25 records
        
        # handle search form/URL parameters:
        if 'city' in self.request.GET:

            city = self.request.GET['city']
            # filter the Results by this parameter
            qs = Voter.objects.filter(city__icontains=city)

        return qs
