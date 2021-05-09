from django.db import models
from account.models import User
from problemInfo.models import ProblemInfo


class SolvedProblem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prob = models.ForeignKey(ProblemInfo, on_delete=models.CASCADE)
    correct = models.BooleanField(verbose_name="풀이 여부")

    class Meta:
        unique_together = (("user", "prob"),)

    def __str__(self):
        return self.user.user_id + ' - ' + self.prob.title
