from django import forms
from .models import Voter
from datetime import datetime

# Generate year choices for date of birth fields
current_year = datetime.now().year
year_choices = [(year, year) for year in range(1900, current_year + 1)]

class VoterFilterForm(forms.Form):
    # Party affiliation filter
    party_affiliation = forms.ChoiceField(
        choices=[('', 'Any')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()],
        required=False,
        label="Party Affiliation"
    )

    # Date of birth filters
    min_date_of_birth = forms.ChoiceField(choices=[('', 'Any')] + year_choices, required=False, label="Born After")
    max_date_of_birth = forms.ChoiceField(choices=[('', 'Any')] + year_choices, required=False, label="Born Before")

    # Voter score filter
    voter_score = forms.ChoiceField(
        choices=[('', 'Any')] + [(score, score) for score in sorted(Voter.objects.values_list('voter_score', flat=True).distinct())],
        required=False,
        label="Voter Score"
    )

    # Election participation filters
    v20state = forms.BooleanField(required=False, label="Voted in 2020 State Election")
    v21town = forms.BooleanField(required=False, label="Voted in 2021 Town Election")
    v21primary = forms.BooleanField(required=False, label="Voted in 2021 Primary Election")
    v22general = forms.BooleanField(required=False, label="Voted in 2022 General Election")
    v23town = forms.BooleanField(required=False, label="Voted in 2023 Town Election")