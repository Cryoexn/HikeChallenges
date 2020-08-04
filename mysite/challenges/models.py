from django.db import models
from django.utils import timezone

# Create your models here.
class Challenge(models.Model):
    challenge_name = models.CharField(max_length=101)
    
    def __str__(self):
        return self.challenge_name

class Mountain(models.Model):
    mnt_name = models.CharField(max_length=100)
    location_city = models.CharField(max_length=100)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    elevation = models.IntegerField(default=0)
    done = models.BooleanField(default=False)
    date_done = models.DateTimeField(null=True, default=None)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def __str__(self):
        return self.mnt_name