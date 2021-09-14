from django.db import models
from django.contrib.auth.models import User

from challenges.models import Mountain, Challenge

class Achievement(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    mnt_completed   = models.ForeignKey(Mountain, on_delete=models.CASCADE, default=None, blank=True, null=True)
    chall_completed = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=None, blank=True, null=True)
    date_completed  = models.DateTimeField(blank=True, null=True, default=None)
    
    # Silence Pylint warnings.
    objects         = models.Manager()

    def __str__(self):
        if self.mnt_completed:
            attr = self.mnt_completed
        else:
            attr = self.chall_completed
            
        return f'({self.user}, {attr})'