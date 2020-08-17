from django.db import models
from django.contrib.auth.models import User
from challenges.models import Mountain, Challenge

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mountain_completed = models.ForeignKey(Mountain, on_delete=models.CASCADE, default=None, blank=True, null=True)
    challenge_completed = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=None, blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):

        if self.mountain_completed:
            attr = self.mountain_completed
        else:
            attr = self.challenge_completed
            
        return f'{self.user.username}, {attr}'