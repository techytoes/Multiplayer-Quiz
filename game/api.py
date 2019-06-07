from django.conf.urls import url
from django.contrib.auth.models import User
from users.models import Question, Users
from game.models import Quiz
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from users.api import validate_user

import json


class GameResource(ModelResource):
    class Meta:
        queryset = Quiz.objects.all()
        quiz_resource = 'quiz'
        allowed_methods = ['get', 'post']

    def prepend_urls(self):
        return [
            url(r"^(?P<quiz_resource>%s)/add%s$" %
                (self._meta.quiz_resource, trailing_slash()),
                self.wrap_view('play_game'), name='api_play_game'),
        ]

    def play_game(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')

        if validate_user(username, password):

            user_id = User.objects.get(username=username).id
            user = Users.objects.get(id=user_id)

            quiz = Quiz(created_by = user)
            quiz.save()
            for q in Question.objects.all():
                if q.user == user:
                    quiz.question.add(q)

            # quiz = {created_by : quiz_question}
            return self.create_response(request, {'status': True, 'Message': 'to be decided'})
