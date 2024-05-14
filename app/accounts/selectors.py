from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from .models import User

# ==================== Users ==================== #
def list_users() -> QuerySet[User]:
    return get_user_model().objects.only('email', 'role')
