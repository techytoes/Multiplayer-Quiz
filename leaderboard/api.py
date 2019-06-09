from django.conf.urls import url
from users.models import Users
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from users.api import validate_user

import json


'''
RESOURCES
'''


class LeaderBoardResource(ModelResource):

    class Meta:
        queryset = Users.objects.all()
        leaderboard_resource = 'leaderboard'
        allowed_methods = ['get', 'post']

    def prepend_urls(self):
        return [
            url(r"^(?P<leaderboard_resource>%s)%s$" %
                (self._meta.leaderboard_resource, trailing_slash()),
                self.wrap_view('leaderboard'), name='api_leaderboard'),
        ]

    # Displays leaderboard
    def leaderboard(self, request, *args, **kwargs):
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')

        if validate_user(username, password):

            user_display = {}

            for u in Users.objects.all():
                user_display[u.name] = u.score

            return self.create_response(request, {
                'status': True,
                'Current Leaderboard': user_display
            })

        else:
            return self.create_response(request, {
                'status': True,
                'Message': 'Invalid Credentials'
            })
