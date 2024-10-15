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
  
  def get_message(self):
    '''Rerurn a QuerySet of all Status Messages on this Profile'''

    #use the ORM to retrieve Status Message for which FK is this Profile
    status = StatusMessage.objects.filter(profile=self)
    return status
  
class StatusMessage(models.Model):
  '''contains the status message of the profile'''
  timestamp = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=False)
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

  def __str__(self):
    '''Return a string representation of this message object.'''
    return f'{self.message}'