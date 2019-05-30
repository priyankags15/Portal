from django.db import models
from django.utils import timezone

class Login_data(models.Model):
    user_name = models.ForeignKey('Citizens')
    email = models.EmailField('Citizens')
    password = models.TextField(null=False, blank=False)
    designation = models.TextField(null=False, blank=False)

class Vote_Casted(models.Model):
    user_name = models.ForeignKey('Citizens')
    casted_year = models.DateField(blank=False,null=False)

class Candidates(models.Model):
    user_name = models.ForeignKey('Citizens')
    vote_count = models.IntegerField(default = 0)
    candidature_date = models.DateField(blank=False)
    agenda = models.TextField(max_length=500, blank=True)
    candidate_designation = models.TextField(null=False, blank=False)
class Election_duration(models.Model):
    election_year = models.IntegerField(blank=False, primary_key = True)
    polling_date  = models.DateField(blank=False)
    candidature_date = models.DateField(blank=False)

class Citizens(models.Model):
    user_name = models. IntegerField(blank=False, primary_key=True)
    First_name = models.TextField(null=False, blank=False)
    Last_name = models.TextField(null=False, blank=False)
    Address = models.TextField(null=False, blank=False)
    email = models.EmailField(max_length=200,null=False, blank=False)
    contact = models.TextField(null=False, blank=False)

# Create your models here.
