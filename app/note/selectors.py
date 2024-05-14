from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Note

User = get_user_model()

@transaction.atomic
def get_notes(*, user_id: int) -> QuerySet[None]:
    user = User.objects.get(id=user_id)
    return Note.objects.filter(writer=user).only('body')
