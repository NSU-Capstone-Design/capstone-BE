from django.db import models
from account.models import User

class Group(models.Model):
    group_name = models.CharField(verbose_name='그룹명', max_length=64, unique=True)
    description = models.TextField(verbose_name='그룹 소개', null=True)
    group_visible = models.BooleanField(verbose_name='공개여부', default=True)
    group_master = models.OneToOneField(User, verbose_name='가입자', on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name


class GroupManage(models.Model):
    group_id = models.OneToOneField(Group, verbose_name='그룹명', on_delete=models.CASCADE)
    member = models.ForeignKey(User, verbose_name='가입자', on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='가입승인여부', default=False)

    def __str__(self):
        return self.group_id