from django.db import models

class problemInfo(models.Model):
    title = models.CharField(max_length=50)
    timeout = models.CharField(max_length=50)
    memory_limit = models.CharField(max_length=50)
    submission = models.CharField(max_length=50)
    correct = models.CharField(max_length=50)
    correct_people = models.CharField(max_length=50)
    correct_answer_rate = models.CharField(max_length=50)
    problem_content = models.TextField(null=True,default='')
    problem_input = models.TextField(null=True,default='')
    problem_output = models.TextField(null=True,default='')
    problem_sampleinput1_data = models.TextField(null=True,default='')
    problem_sampleoutput1_data = models.TextField(null=True,default='')
    problem_sampleinput2_data = models.TextField(null=True,default='')
    problem_sampleoutput2_data = models.TextField(null=True,default='')

    def __str__(self):
        return self.title



