from django.conf.urls import url
from django.contrib.auth.models import User
from users.models import Question, Users
from game.models import Quiz
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from users.api import validate_user

import json


allowed_users = []
class GameResource(ModelResource):
    class Meta:
        queryset = Quiz.objects.all()
        quiz_resource = 'quiz'
        create_resource = 'create'
        play_resource = 'play'
        allowed_methods = ['get', 'post']

    def prepend_urls(self):
        return [
            url(r"^(?P<quiz_resource>%s)/add%s$" %
                (self._meta.quiz_resource, trailing_slash()),
                self.wrap_view('add_quiz'), name='api_add_quiz'),
            url(r"^(?P<create_resource>%s)/game%s$" %
                (self._meta.create_resource, trailing_slash()),
                self.wrap_view('create_game'), name='api_create_game'),
            url(r"^(?P<play_resource>%s)/game%s$" %
                (self._meta.play_resource, trailing_slash()),
                self.wrap_view('play_game'), name='api_play_game'),
            url(r"^(?P<play_resource>%s)/game/submit%s$" %
                (self._meta.play_resource, trailing_slash()),
                self.wrap_view('submit_ans'), name='api_submit_ans'),
        ]

    def add_quiz(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')

        if validate_user(username, password):

            fetch_id = User.objects.get(username=username).id
            user_id = Users.objects.get(id=fetch_id)

            quiz = Quiz(created_by=user_id)
            quiz.save()
            for q in Question.objects.all():
                if q.user_id == user_id:
                    quiz.question.add(q)

            # quiz = {created_by : quiz_question}
            return self.create_response(request, {'status': True, 'Message': 'to be decided'})

    # Allow a user to create game
    def create_game(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        allowed_users = body.get('allowed_users')

        if validate_user(username, password):
            # Returns the link to created Quiz
            return self.create_response(request, {'status': True, 'Game created at ' : '127.0.0.1:8000/api/v2/play/game/'})

    # Allows user to view quiz
    def play_game(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')

        if validate_user(username, password):

            if username not in allowed_users:
                return self.create_response(request, {'status':True, 'Message':'User not allowed to view/play the game'})

            else:
                # Will insert in a dictionary here and create a response once I know how to iterate through quiz.

    # Allows user to submit responses
    def submit_ans(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        responses = body.get('responses')

        if validate_user(username, password):

            if username not in allowed_users:
                return self.create_response(request, {'status':True, 'Message':'User not allowed to view/play the game'})

            else:
                # Check the responses with correct option for those questions
                # And update score accordingly
