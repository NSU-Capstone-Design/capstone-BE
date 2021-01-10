from django.db import models

class QuestionPost(models.Model):
    title = models.CharField()
    content = models.TextField()
    code = models.TextField()
    created_at = models.DateTimeField()