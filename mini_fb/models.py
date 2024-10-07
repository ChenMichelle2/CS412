from django.db import models

# Create your models here.

class Profile(models.Model):
  '''Encapsulates the idea of a profile of a person'''
  first_name = models.TextField(blank=False)
  last_name =  models.TextField(blank=False)
  city = models.TextField(blank=False)
  email = models.TextField(blank=False)
  image_url = models.URLField(blank=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'