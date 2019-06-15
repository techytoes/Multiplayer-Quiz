from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key


models.signals.post_save.connect(create_api_key, sender=User)


class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, default="2000-01-01")
    occupation = models.CharField(max_length=50)
    score = models.BigIntegerField(default=0)
    is_submitted = models.BooleanField(default=False)


class Question(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    question_body = models.CharField(max_length=50)
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    correct = models.IntegerField()

