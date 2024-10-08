## blog/urls.py
## descruption: URL pattern for the blog app
from django.urls import path
from django.conf import settings
from . import views

urlpatterns =[
  path(r'', views.ShowAllView.as_view(), name="show_all_blog" ),
]