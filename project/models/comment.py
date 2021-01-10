from django.db import models
from django.utils import timezone
from .user import *
from .questionpost import *

class Comment(models.Model):
    postID = models.ForeignKey(QuestionPost, on_delete=models.CASCADE)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete= models.CASCADE)
    votes = models.IntegerField()
    created_at = models.DateTimeField()