from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from users.models import Question, Users
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash

import json


# Validating User for correct Credentials
def validate_user(username, password):
    user = User.objects.filter(username=username)
    if user.count() < 1:
        return False
    if not check_password(password, user.first().password):
        return False
    return True


class QuestionResource(ModelResource):
    class Meta:
        queryset = Question.objects.all()
        question_resource = 'question'
        user_resource = 'user'
        allowed_methods = ['get', 'post']

    def prepend_urls(self):
        return [
            url(r"^(?P<question_resource>%s)/add%s$" %
                (self._meta.question_resource, trailing_slash()),
                self.wrap_view('add_question'), name='api_add_question'),
            url(r"^(?P<user_resource>%s)/register%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('register'), name='api_register'),
            url(r"^(?P<user_resource>%s)/login%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('login'), name='api_login'),
        ]

    # Adds Question into the database of a user
    def add_question(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        question_body = body.get('question_body')
        options = body.get('options')
        correct = body.get('correct')

        # Fetch ID of the user
        fetch_id = User.objects.get(username=username).id
        user_id = Users.objects.get(id=fetch_id)

        # Check if the user is valid
        if validate_user(username, password):

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
            score=0
        )
        user_settings.save()
        return self.create_response(request, {'status': True, 'Message': 'Registration Successful'})

    # Login users with previously created account
    def login(self, request, *args, **kwargs):
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

        fetch_id = User.objects.get(username=username).id
        user_id = Users.objects.get(id=fetch_id)

        question_set = {}
        for q in Question.objects.all():

            if q.user_id == user_id:
                question_set[q.question_body] = [q.option1, q.option2, q.option3, q.option4, q.correct]

        resp = {'status': True, 'Questions': question_set}
        return self.create_response(request, resp)
