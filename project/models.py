from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
  '''Encapsulates the idea of a profile of a person'''
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_project')
  image_url = models.URLField(blank=True)

  def __str__(self):
    return f'{self.user.username}'
  

  
class Dragon(models.Model):
  '''encapsulates the idea of a dragon and its attributes'''
  name = models.CharField(max_length=100, unique=True)
  rarity = models.CharField(max_length=50, blank=False, null=True)
  combo = models.CharField(max_length=200, blank= False, null=True)
  incubation = models.DurationField(blank=True, null=True)

  # image url
  image_url = models.URLField(max_length=300, blank=True, null=True)

  def __str__(self):
    return self.name
  
class FavoriteDragon(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorites')
    dragon = models.ForeignKey(Dragon, on_delete=models.CASCADE, related_name='favorited_by')
    added_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile.user.username} - {self.dragon.name}"
  
class Wishlist(models.Model):
   
  '''Links a user's profile to a specific dragon with a breeding combination'''
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='wishlists')
  dragon = models.ForeignKey(Dragon, on_delete=models.CASCADE, related_name='wishlisted_by')
  parent_1 = models.CharField(max_length=100, blank=False)
  parent_2 = models.CharField(max_length=100, blank=False)
  date_added = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f"{self.profile.user} - {self.dragon.name} ({self.parent_1} + {self.parent_2})"