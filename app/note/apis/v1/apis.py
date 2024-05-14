import jwt

from django.conf import settings
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from ...selectors import get_notes
from accounts.apis.v1.permissions import IsAuthenticated


class NoteApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    class OutputNoteSerializer(serializers.Serializer):
        body = serializers.CharField()

    @extend_schema(responses=OutputNoteSerializer)
    def get(self, request: Request, *args, **kwargs):
        try:
            data = jwt.decode(
                jwt=request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'], None),
                key=settings.SECRET_KEY,
                algorithms='HS256'
            )
            notes = get_notes(user_id=data['id'])
        except Exception as ex:
            return Response(
                {'error': f'{ex}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            self.OutputNoteSerializer(notes, many=True).data,
            status=status.HTTP_200_OK
        )