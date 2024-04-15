from .models import *
from .constants import *

class MyBackend:
    def authenticate(self, request, first_name, last_name, password):
        try:
            user = User.objects.get(first_name=first_name, last_name=last_name)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None