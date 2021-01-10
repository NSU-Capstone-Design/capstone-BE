from django.db import models

class IOExam(models.Model):
    input = models.TextField()
    output = models.TextField()
