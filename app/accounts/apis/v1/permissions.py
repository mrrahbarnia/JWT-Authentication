import jwt

from django.core.cache import cache
from django.conf import settings
from rest_framework.request import Request
from rest_framework.permissions import BasePermission
from jwt.exceptions import InvalidSignatureError

class IsAuthenticated(BasePermission):

    def has_permission(self, request: Request, view):
        auth_token = request.COOKIES.get('AUTH_COOKIE')
        if auth_token:
            try:
                data = jwt.decode(jwt=auth_token, key=settings.SECRET_KEY, algorithms="HS256")
                user_id, security_stamp = data['id'], data['security_stamp']
                cached_security = cache.get(f'ss_{user_id}')
                if cached_security == security_stamp:
                    return True
                else:
                    return False

            except InvalidSignatureError:
                return False
        else:
            return False


class IsAdmin(BasePermission):

    def has_permission(self, request: Request, view):
        auth_token = request.COOKIES.get('AUTH_COOKIE')
        if auth_token:
            try:
                data = jwt.decode(jwt=auth_token, key=settings.SECRET_KEY, algorithms="HS256")
                user_id, security_stamp, role = data['id'], data['security_stamp'], data['role']
                cached_security = cache.get(f'ss_{user_id}')
                if cached_security == security_stamp:
                    if role == 'AD':
                        return True
                    return False
                return False

            except InvalidSignatureError:
                return False

        return False