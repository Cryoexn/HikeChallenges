from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    repo_link = models.URLField()

    # Prevent pylink complaints.
    objects = models.Manager()

