from django.db import models

class todo(models.Model):
    index = models.TextField()
    toggle = models.BooleanField(default=False)