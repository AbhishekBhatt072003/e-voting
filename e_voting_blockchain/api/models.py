from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='No data')
    last_name = models.CharField(max_length=255, default='No data')
    date_of_birth = models.CharField(max_length=255, default='No data')
    account_type = models.CharField(max_length=5, default='voter')

    def __str__(self):
        return f"{self.account_type} - {self.first_name} {self.last_name} - {self.date_of_birth}."
class Election(models.Model):
    name = models.CharField(max_length=255, default='No data available')
    start_date = models.CharField(max_length=255, default='No data available')
    end_date = models.CharField(max_length=255, default='No data available')

    def __str__(self):
        return self.name
    
class Candidate(models.Model):
    first_name = models.CharField(max_length=255, default='No data available')
    last_name = models.CharField(max_length=255, default='No data available')
    date_of_birth = models.CharField(max_length=255, default='No data available')
    group_name = models.CharField(max_length=255, default='No data available')
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.group_name}"



class Ballot(models.Model):
    election = models.ForeignKey(Election, on_delete= models.CASCADE)
    title = models.CharField(max_length=255, default='No data available')

    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} voted for {self.candidate} in {self.ballot}"