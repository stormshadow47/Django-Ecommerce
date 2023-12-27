from django.contrib.auth.backends import BaseBackend
from Users.models import UserProfile

class UserProfileAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(email=email)
            if user.is_admin:
                return user
        except UserProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None
        
    def authenticate_header(self, request):
        return 'Bearer realm="UserProfileAuthBackend", error="invalid_token", error_description="Authentication credentials were not provided or are invalid"'

