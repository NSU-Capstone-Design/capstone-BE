from django.db import models
from .user import *
from .group import *
class GroupManage(models.Model):
    group_id = models.ForeignKey(Group, on_delete = models.CASCADE)
    member = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.BooleanField()