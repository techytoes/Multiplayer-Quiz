from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from users.models import Question, Users, Quiz
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
            url(r"^(?P<question_resource>%s)/equip%s$" %
                (self._meta.question_resource, trailing_slash()),
                self.wrap_view('get_equipment'), name='api_get_equipment'),
            url(r"^(?P<question_resource>%s)/switch%s$" %
                (self._meta.question_resource, trailing_slash()),
                self.wrap_view('toggle_equipment'), name='api_toggle_equipment'),
            url(r"^(?P<question_resource>%s)/add%s$" %
                (self._meta.question_resource, trailing_slash()),
                self.wrap_view('add_question'), name='api_add_question'),
            url(r"^(?P<user_resource>%s)/signup%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('register'), name='api_register'),
            url(r"^(?P<user_resource>%s)/login%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('login'), name='api_login'),
            url(r"^(?P<user_resource>%s)/score%s$" %
                (self._meta.user_resource, trailing_slash()),
                self.wrap_view('add_score'), name='api_add_score')
        ]

    # def validate_key(self, body, key):
    #     if not body or key not in body:
    #         result = {'status': False,
    #                   'message': 'Expected equipment {0}'.format(key)}
    #         return result
    #     equipment = Question.objects.filter(id=body[key])
    #     if equipment.count() < 1:
    #         result = {'status': False,
    #                   'message': 'Equipment {0} does not exist'.format(key)}
    #         return result
    #     return {'status': True, 'query': equipment.first()}
    #
    # def get_equipment(self, request, *args, **kwargs):
    #     body = json.loads(request.body)
    #     result = self.validate_key(body, 'id')
    #     if not result['status']:
    #         return self.create_response(request, result)
    #     equipment = result.get('query')
    #     response = {
    #         'name': equipment.name,
    #         'rating': equipment.rating,
    #         'priority': equipment.priority
    #     }
    #     return self.create_response(request, response)

    # def toggle_equipment(self, request, *args, **kwargs):
    #     # equip_id, status
    #     body = json.loads(request.body)
    #     result = self.validate_key(body, 'id')
    #     if not result['status']:
    #         return self.create_response(request, result)
    #     equipment = result.get('query')
    #     equipment_usage = Usage.objects.filter(equipment=equipment)
    #     if equipment_usage.count() < 1:
    #         result = {
    #             'status': False,
    #             'message': '{0}\'s usage does not exist'.format(equipment.name)
    #         }
    #         return self.create_response(request, result)
    #     equipment_usage = equipment_usage.first()
    #     required_state = body.get('state')
    #     if not equipment_usage.state and required_state:
    #         equipment_usage.state = required_state
    #         equipment_usage.started_at = datetime.now().time()
    #         equipment_usage.save()
    #         # TODO: toggle gpio switch
    #         # gpio.turn_on(16, True)
    #     if equipment_usage.state and not required_state:
    #         equipment_usage.state = required_state
    #         equipment_usage.stopped_at = datetime.now().time()
    #         stop_mins = equipment_usage.stopped_at.hour * \
    #             60 + equipment_usage.stopped_at.minute
    #         start_mins = equipment_usage.started_at.hour * \
    #             60 + equipment_usage.started_at.minute
    #         equipment_usage.used_mins += stop_mins - start_mins
    #         equipment_usage.save()
    #         # TODO: toggle gpio switch
    #         # gpio.turn_on(16, False)
    #     result = {
    #         'name': equipment.name,
    #         'state': equipment_usage.state
    #     }
    #     return self.create_response(request, result)

    # def add_score(self, request, *args, **kwargs):
    #     hostname = request.build_absolute_uri('/')
    #     body = json.loads(request.body)
    #     new_score = body.get('score')
    #     user = User.objects.all()
    #     user_settings = Users.objects.filter(user=user.first()).first()
    #     user_settings.score = new_score
    #     user_settings.save()
    #     response = {'status': True, 'redirect': hostname + 'dash/'}
    #     return self.create_response(request, response)

    # Adds Question into the database of a user
    def add_question(self, request, *args, **kwargs):
        hostname = request.build_absolute_uri('/')
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        question_body = body.get('question_body')
        options = body.get('options')
        correct = body.get('correct')

        # Fetch ID of the user
        user_id = User.objects.get(username=username).id

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
            response = {'status': True, 'redirect': hostname + 'dash/'}
            return self.create_response(request, response)

    # Registers New User
    def register(self, request, *args, **kwargs):
        hostname = request.build_absolute_uri('/')
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
        return self.create_response(request, {'status': True, 'redirect': hostname + 'dash/'})

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

        question_set = {}
        for q in Question.objects.all():
            question_set[q.question_body] = [q.option1, q.option2, q.option3, q.option4, q.correct]

        resp = {'status': True, 'question_set': question_set}
        return self.create_response(request, resp)
