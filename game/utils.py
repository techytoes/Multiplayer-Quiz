from game.models import Game, Quiz
from users.utils import fetch_id

'''
HELPER FUNCTIONS
'''


# Checks if the user is allowed to participate in the Game
def is_allowed(creator_user_id, api_key):

    user_name = fetch_id(api_key).name
    for game in Game.objects.all():
        for user in game.allowed_users.all():
            if user.name == user_name:
                return True
    return False
