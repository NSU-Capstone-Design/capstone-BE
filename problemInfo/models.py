from django.db import models


class ProblemInfo(models.Model):
    title = models.CharField(verbose_name="제목", max_length=50)
    level = models.IntegerField(verbose_name="문제 레벨", default=-1)
    timeout = models.CharField(verbose_name="시간 제한", max_length=50)
    memory_limit = models.CharField(verbose_name="메모리 제한", max_length=50)
    submission = models.CharField(verbose_name="제출 수", max_length=50)
    correct = models.CharField(verbose_name="정답 수", max_length=50)
    correct_people = models.CharField(verbose_name="맞은 사람 수", max_length=50)
    correct_answer_rate = models.CharField(verbose_name="정답 비율", max_length=50)
    problem_content = models.TextField(verbose_name="문제 설명", null=True)
    problem_input = models.TextField(verbose_name="문제 입력 설명", null=True)
    problem_output = models.TextField(verbose_name="문제 출력 설명", null=True)

    def __str__(self):
        return self.title


class IOExam(models.Model):
    problem = models.ForeignKey(ProblemInfo, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    io_num = models.IntegerField()
    is_input = models.BooleanField()

    def __str__(self):
        return self.problem.title
