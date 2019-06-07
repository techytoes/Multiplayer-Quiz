from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from users.models import Users, Question


class Quiz(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=50)