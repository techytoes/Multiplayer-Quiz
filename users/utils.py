from users.models import Users
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

'''
HELPER FUNCTIONS
'''


# Validating User for correct Credentials
def validate_user(username, password):
    user = User.objects.filter(username=username)
    if user.count() < 1:
        return False
    if not check_password(password, user.first().password):
        return False
    return True


# Fetch Users object
def fetch_id(username):

    find_id = User.objects.get(username=username).id
    user_id = Users.objects.get(id=find_id)

    return user_id
