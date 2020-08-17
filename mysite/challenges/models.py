from django.db import models
from django.utils import timezone

class Mountain(models.Model):
    mnt_name = models.CharField(max_length=100)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    elevation = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)

    def __str__(self):
        return self.mnt_name

class Challenge(models.Model):
    challenge_name = models.CharField(max_length=101)
    mountains = models.ManyToManyField(Mountain)
    
    def __str__(self):
        return self.challenge_name
