from django.db import models

# Create your models here.
class Voter(models.Model):
  """
  Stores:
  Last Name,First Name,Residential Address - Street Number,Residential Address 
  - Street Name,Residential Address - Apartment Number,Residential Address - 
  Zip Code,Date of Birth,Date of Registration,Party Affiliation,Precinct Number,
  v20state,v21town,v21primary,v22general,v23town,voter_score
  """
  #identification
  last_name = models.TextField()
  first_name = models.TextField()

  #address
  street_num = models.IntegerField()
  street_name = models.TextField()
  apt_num = models.IntegerField()
  zipcode = models.IntegerField()

  #dates
  dob = models.DateField()
  reg_date = models.DateField()

  #voting background(?)
  affiliation = models.CharField(max_length=2)
  precint = models.IntegerField()

  #participation
  state_20 = models.BooleanField()
  town_21 = models.BooleanField()
  primary_21 = models.BooleanField()
  general_22 = models.BooleanField()
  town_23 = models.BooleanField()

  def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.street_num} {self.street_name} Apartment {self.apt_num} {self.zipcode}"

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    Voter.objects.all().delete()
    filename = '/Users/michelle/Desktop/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    #for row in range(5):
        #line = f.readline().strip()
        #fields = line.split(',')
        # show which value in each field
    for line in f:
      fields = line.split(',') # create a list of fields
      try:
        # create a new instance of Result object with this record from CSV
        result = Voter(first_name=fields[2],
                      last_name = fields[1],
                      street_num = fields[3],
                      street_name = fields[4],
                      apt_num = fields[5],
                      zipcode = fields[6]

                    )
        result.save() # save this instance to the database.
        print(f'Created result: {result}')
      except:
          print(f"Exception on {fields}")


  