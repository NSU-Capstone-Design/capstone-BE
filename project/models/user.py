from django.db import models

class User(models.Model):
    ID = models.CharField(primary_key = True)
    password = models.CharField()
    nickname = models.CharField()
    csrf = models.CharField()
    login_token = models.CharField()