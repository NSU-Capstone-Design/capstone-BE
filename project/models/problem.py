from django.db import models

class Problem(models.Model):
    title = models.CharField()
    content = models.TextField()
    algorithm = models.CharField()
    level = models.CharField()
    exp = models.IntegerField()