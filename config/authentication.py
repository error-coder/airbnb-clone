from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class TrustMeBroAuthentication(BaseAuthentication):

    def authenticate(self, request):
        username = request.headers.get('Trust-Me') # username이 TrustMe Header에 존재하면 user가 인증을 시도했다는 의미
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None) # user = request.user
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}") # user가 username을 headers에 보냈지만 잘못된 정보임