from django.db import models
from .user import *

class Group(models.Model):
    master = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    name = models.CharField()
