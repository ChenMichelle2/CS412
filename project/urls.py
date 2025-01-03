# project/urls/py
# Comatins the urls of the project

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import *
from . import views

urlpatterns =[
  path(r'', views.ShowAllDragons.as_view(), name="Show_All_Dragons" ),
  path(r'show_all_dragons/', views.ShowAllDragons.as_view(), name="Show_All_Dragons" ),
  path(r'profile/me/', views.UserProfileView.as_view(), name="Dragon_User_Profile"),
  path(r'create_profile/', CreateUserAndProfile, name = "create profile dragon"),
  path(r'profile/me/add_wishlist', views.AddToWishlistView.as_view(), name ="Add to Wishlist"),
  path(r'profile/me/remove_wishlist',views.RemoveFromWishlistView.as_view(), name = "Remove from Wishlist"),
  path(r'profile/me/fav_drag', views.EditFav.as_view(), name ="Edit Favorite"),
  path(r'about/',views.AboutView.as_view(), name = "About"),
  path(r'profile/me/update', views.UpdateProfileView.as_view(), name = "update profile"),

  path(r'login/',views.CustomLoginView.as_view(template_name='project/login.html'), name = "login"),
  path(r'logout/', views.CustomLogoutView.as_view(), name='logout'),
]