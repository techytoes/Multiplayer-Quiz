from django.conf.urls import url
from users.models import Users
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from users.api import valid_user

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
        api_key = body.get('api_key')

        if not valid_user(request, api_key=api_key):

            return self.create_response(request, {
                'status': True,
                'Message': 'Invalid Credentials'
            })

        else:

            user_display = {}
            for u in Users.objects.all():
                user_display[u.name] = u.score

            return self.create_response(request, {
                'status': True,
                'Current Leaderboard': user_display
            })
