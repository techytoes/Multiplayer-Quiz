from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, default="2000-01-01")
    occupation = models.CharField(max_length=50)
    score = models.BigIntegerField(default=0)


class Question(models.Model):
    user_id = models.IntegerField()
    question_body = models.CharField(max_length=50)
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    correct = models.IntegerField()


class Quiz(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
