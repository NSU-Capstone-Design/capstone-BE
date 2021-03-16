from django.db import models


class ProblemInfo(models.Model):
    title = models.CharField(verbose_name="제목", max_length=50)
    level = models.IntegerField(default=-1)
    timeout = models.CharField(max_length=50)
    memory_limit = models.CharField(max_length=50)
    submission = models.CharField(max_length=50)
    correct = models.CharField(max_length=50)
    correct_people = models.CharField(max_length=50)
    correct_answer_rate = models.CharField(max_length=50)
    problem_content = models.TextField(null=True)
    problem_input = models.TextField(null=True)
    problem_output = models.TextField(null=True)
    imgurl = models.TextField(null=True)

    def __str__(self):
        return self.title


class IOExam(models.Model):
    problem = models.ForeignKey(ProblemInfo, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    io_num = models.IntegerField()
    is_input = models.BooleanField()

    def __str__(self):
        return self.problem.title
