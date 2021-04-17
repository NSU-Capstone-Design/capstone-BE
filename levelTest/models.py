from django.db import models
from account.models import User
from problemInfo.models import ProblemInfo
from django.utils.translation import gettext_lazy as _


class TestProblem(models.Model):
    DIFFICULTLY = (
        ("상", "전혀 감이 안잡힌다."),
        ("중", "시도해볼 수 있을 것 같다."),
        ("하", "충분히 풀 수 있었다."),
        ("-", "아직 평가하지 않음")
    )
    number = models.IntegerField(verbose_name="번호")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    weight = models.IntegerField(_("가중치"))
    problem = models.ForeignKey(ProblemInfo, on_delete=models.PROTECT, null=True)
    evaluation = models.CharField(verbose_name="평가", max_length=50, choices=DIFFICULTLY, default="-")

    def __str__(self):
        return f'{self.user.user_id} | {self.problem.title} | {str(self.number)}'


class Score(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    score = models.IntegerField(default=-1)

    def __str__(self):
        return f'{self.user.user_id} | {self.score}'
