from django.shortcuts import render
from django.views.generic import *
from .models import *
from .forms import *
from django.db.models.query import QuerySet
from typing import Any

# Create your views here.
## formdata.urls.py
## define the URLs for this app

class ShowVoters(ListView):
  model= Voter
  template_name = 'voter_analytics/voters.html'
  context_object_name = 'voters'
  paginate_by = 50
    
  #def get_queryset(self):
        
  #      qs = super().get_queryset()
  #      #return qs[:25]
  #      return qs
  def get_queryset(self):
        # Start with the base queryset of all voters
        qs = super().get_queryset()

        # Initialize the form with GET data
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            # Apply filters based on form data
            party = form.cleaned_data.get('party_affiliation')
            if party:
                qs = qs.filter(party_affiliation=party)

            min_dob = form.cleaned_data.get('min_date_of_birth')
            if min_dob:
                qs = qs.filter(date_of_birth__year__gte=min_dob)

            max_dob = form.cleaned_data.get('max_date_of_birth')
            if max_dob:
                qs = qs.filter(date_of_birth__year__lte=max_dob)

            voter_score = form.cleaned_data.get('voter_score')
            if voter_score:
                qs = qs.filter(voter_score=voter_score)

            for election_field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(election_field):
                    qs = qs.filter(**{election_field: True})

        return qs

  def get_context_data(self, **kwargs):
        # Add the form to the context
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context

