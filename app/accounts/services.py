import jwt
import uuid

from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.conf import settings
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .models import User

user_model = get_user_model()

def create_unique_security_stamp() -> str:
    return str(uuid.uuid4())

# ==================== JWT Tokens ==================== #
def create_token_for_user(*, user: User, security_stamp: str) -> str:
    """
    Create custom encrypted token for authenticated user with all it's information.
    """
    custom_token = jwt.encode(
        payload={
            "email": user.email,
            "role": user.role,
            "id": user.pk,
            "security_stamp": security_stamp,
        },
        key=settings.SECRET_KEY,
        algorithm="HS256"
    )
    return custom_token

# ==================== Authentication ==================== #
def set_security_stamp(*, user_id: int, security_stamp: str) -> None:
    """
    Set security stamp in redis memory with refresh_token life time for timeout.
    It will use for validating user activities,
    roles, etc... after each request in the custom middleware.
    """
    refresh_token_lifetime_seconds: timedelta = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    cache.set(
        key=f'ss_{user_id}',
        value=security_stamp,
        timeout=refresh_token_lifetime_seconds.total_seconds()
    )

def validate_uniqueness_email(*, email: str) -> bool:
    """
    Check unique constraint for user emails and it returns boolean.
    """
    return user_model.objects.filter(email=email).exists()


def register_user(
    *, email: str, password: str
) -> User:
    """
    Create user with the provided info and also sending
    created_user info to set_security_stamp function.
    """
    user: User = user_model.objects.create_user(
        email=email,
        password=password
    )

    return user

def set_token_to_cookies(*, user: User, security_stamp: str, response: Response) -> None:
    """
    Setting httpOnly and Strict samesite cookies for authenticated users.
    """
    data = create_token_for_user(user=user, security_stamp=security_stamp)
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=data,
        max_age=(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']).seconds,
        secure=False,
        httponly=True,
        samesite='Strict'
    )
    return response

@transaction.atomic
def login_user(*, email: str, password: str) -> User | None:
    """
    Login and set security_stamp to redis for each user.
    """
    security_stamp: str = create_unique_security_stamp()
    authenticated_user: User = authenticate(username=email, password=password)
    set_security_stamp(
        user_id=authenticated_user.pk, security_stamp=security_stamp
    )
    return authenticated_user, security_stamp

@transaction.atomic
def change_user_role(*, user_id: int, new_role: str) -> User:
    try:
        user: User = user_model.objects.get(id=user_id)
    except user_model.DoesNotExist:
        raise APIException('There is no user with the provided id.')
    user.role = new_role
    user.save(update_fields=['role'])
    cache.delete(key=f'ss_{user_id}')
    return user
