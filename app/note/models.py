from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Note(models.Model):
    writer = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True
    )
    body = models.CharField(max_length=1000)
