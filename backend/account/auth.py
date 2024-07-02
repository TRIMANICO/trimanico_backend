from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)

            if user.check_password(password):
                return user
            else:
                return None

        except User.DoesNotExist:
            return None
