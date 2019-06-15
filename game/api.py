from django.conf.urls import url
from users.models import Question, Users
from game.models import Quiz, Game
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from users.utils import valid_user, fetch_id
from game.utils import is_allowed

import json

'''
RESOURCES
'''


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
        api_key = body.get('api_key')

        if not valid_user(request, api_key):

            return self.create_response(request, {
                'status': False,
                'Message': 'Invalid Credentials'
            })

        else:
            user_id = fetch_id(api_key=api_key)
            quiz = Quiz(created_by=user_id)
            quiz.save()
            for q in Question.objects.all():
                if q.user_id == user_id:
                    quiz.question.add(q)

            return self.create_response(request, {
                'status': True,
                'Message': 'Quiz created by:' + user_id.name
            })

    # Allow a user to create game
    def create_game(self, request, *args, **kwargs):
        body = json.loads(request.body)
        api_key = body.get('api_key')
        allowed_users = body.get('allowed_users')

        if not valid_user(request, api_key):

            return self.create_response(request, {
                'status': False,
                'Message': 'Invalid Credentials'
            })

        else:
            # Fetch quiz object for creator user
            user_id = fetch_id(api_key)
            quiz = Quiz.objects.get(created_by=user_id)

            game = Game(quiz=quiz)
            game.save()

            for name in allowed_users:
                user = Users.objects.get(name=name)
                game.allowed_users.add(user)

            # Returns the link to created Quiz
            return self.create_response(request, {
                'status': True,
                'Message': 'Game created at - https://127.0.0.1:8000/api/v2/play/game/'
            })

    # Allows user to view quiz
    def play_game(self, request, *args, **kwargs):
        body = json.loads(request.body)
        api_key = body.get('api_key')
        created_by = body.get('created_by')

        # fetch player Users object
        player_user_id = fetch_id(api_key)

        # fetch creator Users Object
        creator_user_id = Users.objects.get(name=created_by)

        if not valid_user(request, api_key):

            return self.create_response(request, {
                'status': True,
                'Message': 'Invalid Credentials'
            })

        else:
            if not is_allowed(creator_user_id, api_key):
                return self.create_response(request, {
                    'status':False,
                    'Message':'User not allowed to view/play the game'
                })

            else:

                quiz = {}
                for j in Quiz.objects.get(created_by=creator_user_id).question.all():
                    quiz[j.question_body] = [j.option1, j.option2, j.option3, j.option4]

                return self.create_response(request, {
                    'status': True,
                    'Message': 'Welcome : ' + player_user_id.name,
                    'Quiz-Questions': quiz
                })

    # Allows user to submit responses
    def submit_ans(self, request, *args, **kwargs):
        body = json.loads(request.body)
        api_key = body.get('api_key')
        created_by = body.get('created_by')
        responses = body.get('responses')

        # fetch player current score
        player_user_id = fetch_id(api_key)
        player_score = player_user_id.score

        # fetch creator Users Object
        creator_user_id = Users.objects.get(name=created_by)
        creator_quiz = Quiz.objects.get(created_by=creator_user_id)

        if not valid_user(request, api_key):

            return self.create_response(request, {
                'status': True,
                'Message': 'Invalid Credentials'
            })

        else:

            if not is_allowed(creator_user_id, api_key):
                return self.create_response(request, {
                    'status': False,
                    'Message':'User not allowed to view/play the game'
                })

            elif player_user_id.is_submitted:
                return self.create_response(request, {
                    'status': True,
                    'Message': 'Responses submitted already. Go to leader-board to view scores.',
                })

            else:

                question_set = creator_quiz.question.all().order_by('id').reverse()
                for q in range(question_set.count()):
                    if responses[q] == question_set[q].correct:
                        player_score += 1

                player_user_id.score = player_score
                player_user_id.is_submitted = True
                player_user_id.save()

                return self.create_response(request, {
                    'status': True,
                    'Message': 'Responses submitted for :' + player_user_id.name,
                })
