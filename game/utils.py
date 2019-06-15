from game.models import Game, Quiz
from users.utils import fetch_id

'''
HELPER FUNCTIONS
'''


# Checks if the user is allowed to participate in the Game
def is_allowed(creator_user_id, api_key):

    user_name = fetch_id(api_key)
    for game in Game.objects.all():
        if game.quiz.created_by == creator_user_id and user_name in game.allowed_users.all():
            return True
    return False
