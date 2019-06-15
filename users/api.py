from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from users.models import Question, Users
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from tastypie.models import ApiKey
from users.utils import fetch_id, valid_user
from users.authentication import KeyAuthentication

import json

'''
RESOURCES
'''


class QuestionResource(ModelResource):
    class Meta:
        queryset = Question.objects.all()
        question_resource = 'question'
        user_resource = 'user'
        allowed_methods = ['get', 'post']
        authentication = KeyAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<question_resource>%s)/add%s$" %
                (self._meta.question_resource, trailing_slash()),
                self.wrap_view('add_question'), name='api_add_question'),
            url(r"^(?P<user_resource>%s)/register%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('register'), name='api_register'),
            url(r"^(?P<user_resource>%s)/key%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('fetch_key'), name='api_fetch_key'),
            url(r"^(?P<user_resource>%s)/login%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('login'), name='api_login'),
        ]

    # Get Unique API-key for user's credentials which can be used as a token.
    def fetch_key(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        if username:
            user = User.objects.filter(username=username)
        if user.count() < 1:
            resp = {'status': False, 'message': 'User does not exists'}
            return self.create_response(request, resp)
        if not check_password(password, user.first().password):
            resp = {'status': False, 'message': 'incorrect password'}
            return self.create_response(request, resp)
        api_key = ApiKey.objects.get(user=User.objects.get(username=username))
        return self.create_response(request, {
            'status': True,
            'api_key': api_key,
        })

    # Registers New User
    def register(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        name = body.get('name')
        date_of_birth = body.get('date_of_birth')
        occupation = body.get('occupation')
        email = body.get('email')
        password = body.get('password')
        user = User.objects.filter(username=username)
        if user.count() > 0:
            resp = {'status': False, 'message': 'Username already exists'}
            return self.create_response(request, resp)
        user = User.objects.filter(username=email)
        if user.count() > 0:
            resp = {'status': False, 'message': 'Email already in use'}
            return self.create_response(request, resp)
        user = User.objects.create_user(
            username,
            email,
            password
        )
        user.save()
        user_settings = Users(
            user=user,
            name=name,
            date_of_birth=date_of_birth,
            occupation=occupation,
            score=0,
            is_submitted=False,
        )
        user_settings.save()
        return self.create_response(request, {'status': True, 'Message': 'Registration Successful'})

    # Login users with previously created account
    def login(self, request, *args, **kwargs):
        body = json.loads(request.body)
        # username = body.get('username')
        api_key = body.get('api_key')

        if not valid_user(request, api_key):
            return self.create_response(request, {
                'status': False,
                'Message': "User Unauthorised",
            })

        else:
            user_id = fetch_id(api_key)
            question_set = {}
            for q in Question.objects.all():

                if q.user_id == user_id:
                    question_set[q.question_body] = [q.option1, q.option2, q.option3, q.option4, q.correct]

            resp = {'status': True, 'Questions': question_set, 'Message': 'Welcome ' + user_id.name}
            return self.create_response(request, resp)

    # Adds Question into the database of a user
    def add_question(self, request, *args, **kwargs):
        body = json.loads(request.body)
        api_key = body.get('api_key')
        question_body = body.get('question_body')
        options = body.get('options')
        correct = body.get('correct')

        # if the user is invalid
        if not valid_user(request, api_key):
            return self.create_response(request, {
                'status': False,
                'Message': "User Unauthorised",
            })

        else:
            user_id = fetch_id(api_key)
            question = Question(
                user_id=user_id,
                question_body=question_body,
                option1=options[0],
                option2=options[1],
                option3=options[2],
                option4=options[3],
                correct=correct
            )
            question.save()
            response = {'status': True, 'Message': 'Question Added Successfully'}
            return self.create_response(request, response)