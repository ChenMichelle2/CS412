from django.db import models
from django.utils import timezone

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
    statusMessage = StatusMessage.objects.filter(profile=self)
    return statusMessage
  
  def get_friends(self):
    '''Returns a list of Profiles who are friends with this Profile'''  
    friends_as_profile1 = Friend.objects.filter(profile1=self)
    friends_as_profile2 = Friend.objects.filter(profile2=self)
  
    friends = [relation.profile2 for relation in friends_as_profile1]
    friends += [relation.profile1 for relation in friends_as_profile2]

    return friends
  
  def get_friend_suggestions(self):
    '''Returns a QuerySet of Profiles that are not currently friends with this Profile and excludes itself'''

    # Get IDs of current friends
    friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
    friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
    friend_ids = set(friends_as_profile1).union(friends_as_profile2)

    # Add the current profile's ID to the set of IDs to exclude
    friend_ids.add(self.id)

    # Return a QuerySet of profiles that are not in the friend_ids set
    return Profile.objects.exclude(id__in=friend_ids)
  
  def add_friend(self, other):
    '''Adds a friend relationship between self and another Profile, if it does not already exist'''
      # Check for self-friending
    if self == other:
      raise ValueError("A profile cannot friend itself.")

    # Checks if a Friend relationship already exists 
    friend_exists = Friend.objects.filter(
      (models.Q(profile1=self) & models.Q(profile2=other)) |
      (models.Q(profile1=other) & models.Q(profile2=self))        
      ).exists()

    if not friend_exists:         
      Friend.objects.create(profile1=self, profile2=other, timestamp=timezone.now())
      return True  # Return True if a new friendship was created

    return False  # Return False if a friendship already exists
  
class StatusMessage(models.Model):
  '''contains the status message of the profile'''
  timestamp = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=False)
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

  def get_images(self):
    '''returns a QuerySet of all related images'''    
    return self.images.all()  # This returns a QuerySet of all related images

  def __str__(self):
    '''Return a string representation of this message object.'''
    return f'{self.message}'
  
class Image(models.Model):
  '''contains image files for status message'''
  image_file = models.ImageField(upload_to='status_images/')
  uploaded_at = models.DateTimeField(auto_now=True)
  status_message = models.ForeignKey(StatusMessage, related_name='images', on_delete=models.CASCADE)

  def __str__(self):
    return f"Image for StatusMessage ID {self.status_message.id} uploaded at {self.uploaded_at}"

class Friend(models.Model):
  '''encapsulates the idea of an edge connecting two nodes within the social network'''
  profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
  profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
  timestamp = models.DateTimeField(default=timezone.now)

  def __str__(self):
        return f"{self.profile1} & {self.profile2}"
