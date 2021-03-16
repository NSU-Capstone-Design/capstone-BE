from django.db import models

class problemInfo(models.Model):
    title = models.CharField(max_length=50)
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
    title = models.CharField(max_length=50)
    problem_sampleinput1_data = models.TextField(null=True)
    problem_sampleoutput1_data = models.TextField(null=True)
    problem_sampleinput2_data = models.TextField(null=True)
    problem_sampleoutput2_data = models.TextField(null=True)
    problem_sampleinput3_data = models.TextField(null=True)
    problem_sampleoutput3_data = models.TextField(null=True)
    problem_sampleinput4_data = models.TextField(null=True)
    problem_sampleoutput4_data = models.TextField(null=True)
    problem_sampleinput5_data = models.TextField(null=True)
    problem_sampleoutput5_data = models.TextField(null=True)
    problem_sampleinput6_data = models.TextField(null=True)
    problem_sampleoutput6_data = models.TextField(null=True)
    problem_sampleinput7_data = models.TextField(null=True)
    problem_sampleoutput7_data = models.TextField(null=True)
    problem_sampleinput8_data = models.TextField(null=True)
    problem_sampleoutput8_data = models.TextField(null=True)
    problem_sampleinput9_data = models.TextField(null=True)
    problem_sampleoutput9_data = models.TextField(null=True)
    problem_sampleinput10_data = models.TextField(null=True)
    problem_sampleoutput10_data = models.TextField(null=True)

    def __str__(self):
        return self.title



