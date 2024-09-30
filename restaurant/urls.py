## formdata.urls.py
## define the URLs for this app

from django.urls import path
from django.conf import settings
from . import views

#define a list of valid URL patterns:
urlpatterns =[
  path(r'', views.main, name="main"),
  path(r'submit', views.submit,name="submit" ),
  path(r'order', views.order, name="order"),
]