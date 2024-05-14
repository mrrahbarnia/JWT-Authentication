from django.urls import path

from . import apis

urlpatterns =[
    path('', apis.NoteApiView.as_view(), name='notes_api')
]