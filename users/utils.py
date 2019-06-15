from users.models import Users
from django.contrib.auth.models import User
from users.authentication import KeyAuthentication

'''
HELPER FUNCTIONS
'''


# Validating User for correct Credentials
def valid_user(request, api_key):

    auth = KeyAuthentication()
    if auth.get_key(request, api_key=api_key) is not True:
        return False
    return True


# Fetch Users object
def fetch_id(api_key):

    for u in User.objects.all():
        if u.api_key.key == api_key:
            find_id = u.id

    user_id = Users.objects.get(id=find_id)
    return user_id
