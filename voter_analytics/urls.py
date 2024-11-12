from django.urls import path
from django.conf import settings
from . import views

#define a list of valid URL patterns:
urlpatterns =[
  path(r'', views.ShowVoters.as_view(), name="home"),
  path(r'voters', views.ShowVoters.as_view(), name = "voters"),
  path(r'voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter_details'),
  path(r'graphs', views.VoterGraphView.as_view(), name = "graphs")
]