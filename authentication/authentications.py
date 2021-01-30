from rest_framework.authentication import BaseAuthentication
from .models import User, Token


class CustomAuth(BaseAuthentication):
    def authenticate(self, request):
        authorization = request.headers.get('Authorization')
        if not authorization:
            return None

        if authorization:
            authorization = authorization.split(' ')[1]

        token = Token.objects.filter(token=authorization).first()
        if not token:
            return None

        if token:
            user = token.user

        return (user, None)
