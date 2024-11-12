from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Represents a registered voter with residential and registration details.
    '''
    # Identification
    last_name = models.TextField()
    first_name = models.TextField()
    residential_street_number = models.TextField()
    residential_street_name = models.TextField()
    residential_apartment_number = models.TextField(blank=True, null=True)
    residential_zip_code = models.TextField()
    
    # Personal and registration details
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    
    # Participation in recent elections
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} (Precinct: {self.precinct_number}, Party: {self.party_affiliation}, Score: {self.voter_score})'
    


def load_data():
    '''Load data records from a CSV file into Voter model instances.'''
    
    # Clear existing records in the database:
    Voter.objects.all().delete()
    
    # Path to the CSV file
    filename = '/Users/michelle/Desktop/newton_voters.csv'
    f = open(filename)
    headers = f.readline()  # Read and discard the headers
    print(headers)

    for line in f:
        try:
            fields = line.strip().split(',')  # Create a list of fields and strip whitespace

            # Create a new instance of Voter with values from the CSV file
            voter = Voter(
                    last_name=fields[1],
                    first_name=fields[2],
                    residential_street_number=fields[3],
                    residential_street_name=fields[4],
                    residential_apartment_number=fields[5] if fields[5] else None,
                    residential_zip_code=fields[6],
                    date_of_birth=fields[7] if fields[7] else None,
                    date_of_registration=fields[8] if fields[8] else None,
                    party_affiliation=fields[9].strip(),
                    precinct_number=fields[10].strip(),
                    v20state=fields[11].strip().lower() == 'true',
                    v21town=fields[12].strip().lower() == 'true',
                    v21primary=fields[13].strip().lower() == 'true',
                    v22general=fields[14].strip().lower() == 'true',
                    v23town=fields[15].strip().lower() == 'true',
                    voter_score = fields[16]
                )
            voter.save()  # Save this instance to the database
            print(f'Created voter: {voter}')

        except Exception as e:
            print(f"Exception on {fields}: {e}")