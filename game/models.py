from django.db import models
from users.models import Users, Question

import uuid


class Quiz(models.Model):
    quiz_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ManyToManyField(Question)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)


class Game(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    allowed_users = models.CharField(max_length=50)