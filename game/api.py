from django.conf.urls import url
from django.contrib.auth.models import User
from users.models import Question, Users
from game.models import Quiz, Game
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from users.api import validate_user

import json


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

            return self.create_response(request, {'status': True, 'Message': 'Quiz created by:' + user_id.name})

    # Allow a user to create game
    def create_game(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        users_allowed = body.get('allowed_users')

        allowed_users = " ".join(i for i in users_allowed)

        if validate_user(username, password):

            # Fetch quiz object for creator user
            fetch_id = User.objects.get(username=username).id
            user_id = Users.objects.get(id=fetch_id)
            quiz = Quiz.objects.get(created_by=user_id)

            game = Game(
                quiz=quiz,
                allowed_users=allowed_users,
            )
            game.save()
            # Returns the link to created Quiz
            return self.create_response(request, {
                'status': True,
                'Message': 'Game created at - https://127.0.0.1:8000/api/v2/play/game/'
            })

    # Allows user to view quiz
    def play_game(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        created_by = body.get('created_by')

        # fetch player Users object
        player_fetch_id = User.objects.get(username=username).id
        player_user_id = Users.objects.get(id=player_fetch_id)

        # fetch creator Users Object
        creator_user_id = Users.objects.get(name=created_by)
        creator_quiz = Quiz.objects.get(created_by=creator_user_id)

        if validate_user(username, password):

            users_allowed = Game.objects.get(quiz=creator_quiz).allowed_users
            if username not in users_allowed:
                return self.create_response(request, {
                    'status':True,
                    'Message':'User not allowed to view/play the game'
                })

            else:
                
                quiz = {}
                for i in Quiz.objects.all():

                    if i.created_by == creator_user_id:
                        for j in i.question.all():
                            quiz[j.question_body] = [j.option1, j.option2, j.option3, j.option4]

                return self.create_response(request, {
                    'status': True,
                    'Message': 'Welcome : ' + player_user_id.name,
                    'Quiz-Questions': quiz
                })

    # # Allows user to submit responses
    # def submit_ans(self, request, *args, **kwargs):
    #     body = json.loads(request.body)
    #     username = body.get('username')
    #     password = body.get('password')
    #     responses = body.get('responses')
    #
    #     if validate_user(username, password):
    #
    #         if username not in users_allowed:
    #             return self.create_response(request, {'status':True, 'Message':'User not allowed to view/play the game'})
    #
    #         else:
    #             # Check the responses with correct option for those questions And update score accordingly
