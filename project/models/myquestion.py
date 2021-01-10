from django.db import models
from .user import *
from .questionpost import *

class MyQuestion(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    question = models.ForeignKey(QuestionPost, on_delete = models.CASCADE)