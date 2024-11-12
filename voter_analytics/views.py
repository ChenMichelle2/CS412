from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.db.models.query import QuerySet
from typing import Any
## new imports:
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
from datetime import datetime
from django.db.models import Count

# Create your views here.
## formdata.urls.py
## define the URLs for this app

class ShowVoters(ListView):
    model= Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['year_options'] = [str(year) for year in range(1900, datetime.now().year + 1)]
        context['voter_score_options'] = [str(score) for score in range(0, 6)]
        
        return context
    def get_queryset(self):
        queryset = Voter.objects.all()

        # Filters
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state') == 'on'
        v21town = self.request.GET.get('v21town') == 'on'
        v21primary = self.request.GET.get('v21primary') == 'on'
        v22general = self.request.GET.get('v22general') == 'on'
        v23town = self.request.GET.get('v23town') == 'on'

        # Apply filters if specified
        if party_affiliation:
            queryset = queryset.filter(party_affiliation= party_affiliation)
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_dob))
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_dob))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        return queryset
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

    def get_queryset(self):
        
        qs = super().get_queryset()
        return qs

class VoterGraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    def get_filtered_queryset(self):
        queryset = Voter.objects.all()

        # Get filter parameters from the request
        party_affiliation = self.request.GET.get('party_affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state') == 'on'
        v21town = self.request.GET.get('v21town') == 'on'
        v21primary = self.request.GET.get('v21primary') == 'on'
        v22general = self.request.GET.get('v22general') == 'on'
        v23town = self.request.GET.get('v23town') == 'on'

        # filters
        if party_affiliation:
            queryset = queryset.filter(party_affiliation__iexact=party_affiliation)
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_dob))
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_dob))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #options for dropdown list in filter
        context['year_options'] = [str(year) for year in range(1900, datetime.now().year + 1)]
        context['voter_score_options'] = [str(score) for score in range(0, 6)]
        
        # Apply filters from the form
        queryset = self.get_filtered_queryset()

        # Histogram for Year of Birth Distribution
        # Convert birth_years to a list to use list.count() correctly
        birth_years = list(queryset.values_list('date_of_birth__year', flat=True))

        # Calculate birth year counts
        birth_year_counts = {year: birth_years.count(year) for year in set(birth_years)}
        birth_year_labels = sorted(birth_year_counts.keys())
        birth_year_values = [birth_year_counts[year] for year in birth_year_labels]

        birth_year_histogram = go.Bar(x=birth_year_labels, y=birth_year_values)
        birth_year_div = plotly.offline.plot({'data': [birth_year_histogram]},
                                             auto_open=False,
                                             output_type='div')

        # Pie Chart for Party Affiliation Distribution
        party_data = queryset.values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_labels = [item['party_affiliation'] for item in party_data]
        party_counts = [item['count'] for item in party_data]

        party_pie_chart = go.Pie(labels=party_labels, values=party_counts)
        party_affiliation_div = plotly.offline.plot({'data': [party_pie_chart]},
                                                    auto_open=False,
                                                    output_type='div')

        # Histogram for Election Participation
        election_participation = {
            '2020 State Election': queryset.filter(v20state=True).count(),
            '2021 Town Election': queryset.filter(v21town=True).count(),
            '2021 Primary Election': queryset.filter(v21primary=True).count(),
            '2022 General Election': queryset.filter(v22general=True).count(),
            '2023 Town Election': queryset.filter(v23town=True).count(),
        }
        election_labels = list(election_participation.keys())
        election_counts = list(election_participation.values())

        election_histogram = go.Bar(x=election_labels, y=election_counts)
        election_participation_div = plotly.offline.plot({'data': [election_histogram]},
                                                         auto_open=False,
                                                         output_type='div')

        # Add graphs to context
        context['birth_year_div'] = birth_year_div
        context['party_affiliation_div'] = party_affiliation_div
        context['election_participation_div'] = election_participation_div

        return context

    