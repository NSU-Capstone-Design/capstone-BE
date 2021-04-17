from django.db import models
from account.models import User
from django.conf import settings


class Group(models.Model):
    group_name = models.CharField(verbose_name='그룹명', max_length=64)
    introduce = models.TextField(verbose_name='그룹 소개', null=True)
    group_visible = models.BooleanField(verbose_name='공개여부', default=True)
    group_master = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='그룹장', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group_name', 'group_master'],
                name='group_name__master_class__restraint'
            )
        ]

    def __str__(self):
        return '그룹명: ' + self.group_name + ', 그룹장: ' + self.group_master.nickname


class GroupManage(models.Model):
    group_id = models.ForeignKey(Group, verbose_name='그룹명', on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='가입자', on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='가입승인여부', default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group_id', 'member'],
                name='group_id__member__restraint'
            )
        ]

    def __flag(self):
        if self.status:
            return 'O'
        return 'X'

    def __str__(self):
        return self.group_id.group_name + ', user: ' + self.member.nickname + ', 가입승인여부: ' + self.__flag()