import jwt

from typing import Any
from django.core.validators import MinLengthValidator
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from .permissions import IsAuthenticated, IsAdmin
from ...models import User
from ...validators import email_validator
from ...selectors import list_users
from ...services import (
    validate_uniqueness_email,
    register_user,
    login_user,
    set_token_to_cookies,
    change_user_role
)


class RegisterApiView(APIView):

    class OutputRegisterSerializer(serializers.Serializer):
        email = serializers.CharField(validators=[email_validator])

    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.CharField(validators=[email_validator])
        password = serializers.CharField(validators=(MinLengthValidator(limit_value=8), ))
        confirm_password = serializers.CharField()

        def validate_email(self, email):
            if validate_uniqueness_email(email=email):
                raise serializers.ValidationError(
                    'There is an active user with the provided email.',
                    code='email_uniqueness'
                )
            return email

        def validate(self, attrs):
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            if password != confirm_password:
                raise serializers.ValidationError(
                    "Passwords don't match.",
                    code='password_not_match'
                )
            return attrs

    @extend_schema(
            request=InputRegisterSerializer,
            responses=OutputRegisterSerializer
    )
    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        input_serializer = self.InputRegisterSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            registered_user = register_user(
                email=input_serializer.validated_data.get('email'),
                password=input_serializer.validated_data.get('password')
            )
        except Exception as ex:
            # TODO: logging
            return Response(
                {'error': f'{ex}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            self.OutputRegisterSerializer(registered_user).data,
            status=status.HTTP_201_CREATED
        )


class LoginApiView(APIView):

    class InputLoginSerializer(serializers.Serializer):
        email = serializers.CharField(validators=(email_validator, ))
        password = serializers.CharField(validators=(MinLengthValidator(limit_value=8), ))

    @extend_schema(request=InputLoginSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        input_serializer = self.InputLoginSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        response = Response()
        try:
            authenticated_user, security_stamp = login_user(
                email=input_serializer.validated_data.get('email', None),
                password=input_serializer.validated_data.get('password', None)
            )
            if authenticated_user:
                safe_response: Response = set_token_to_cookies(
                    user=authenticated_user,
                    security_stamp=security_stamp,
                    response=response
                )
                safe_response.status_code = status.HTTP_200_OK
                return safe_response
        except Exception as ex:
            # TODO: logging
            return Response(
                {'error': 'There is no active user with the provided info.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class MyProfileApiView(APIView):
    permission_classes = [IsAuthenticated]

    class MyProfileOutputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        role = serializers.CharField()

    @extend_schema(responses=MyProfileOutputSerializer)
    def get(self, request: Request, format=None) -> Response:
        try:
            data = jwt.decode(
                jwt=request.COOKIES.get('AUTH_COOKIE', None),
                key=settings.SECRET_KEY,
                algorithms='HS256'
            )
            data = {'email': data['email'], 'role': data['role']}
            return Response(self.MyProfileOutputSerializer(data).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {'error': f'{ex}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListUsersApiView(APIView):
    permission_classes = [IsAdmin]

    class ListUsersOutputSerializer(serializers.Serializer):
        email = serializers.CharField()
        role = serializers.CharField()

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            users = list_users()
        except Exception as ex:
            return Response(
                {'error': f'{ex}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            self.ListUsersOutputSerializer(users, many=True).data,
            status=status.HTTP_200_OK
        )


class ChangeRolesApiView(APIView):
    permission_classes = [IsAdmin]

    class ChangeRolesInputSerializer(serializers.Serializer):
        new_role = serializers.ChoiceField(choices=User.Roles)
    
    class ChangeRolesOutputSerializer(serializers.Serializer):
        email = serializers.CharField()
        role = serializers.CharField()

    @extend_schema(
            request=ChangeRolesInputSerializer,
            responses=ChangeRolesOutputSerializer
    )
    def post(
            self, request: Request, id: int = None, *args: Any, **kwargs: dict
    ) -> Response:
        input_serializer = self.ChangeRolesInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            modified_user = change_user_role(
                user_id=id,
                new_role=input_serializer.validated_data.get('new_role', None)
            )
        except Exception as ex:
            return Response(
                {'error': f'{ex}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            self.ChangeRolesOutputSerializer(modified_user).data,
            status=status.HTTP_200_OK
        )
