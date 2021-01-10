from django.db import models
from .user import *
from .problem import *

class ProbManage(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    solved_check = models.BooleanField()
    marked_check = models.BooleanField()
    problem = models.ForeignKey(Problem, on_delete= models.CASCADE)