import re

from django.core.exceptions import ValidationError


def email_validator(email: str):
    email_regex = re.compile("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    if email_regex.search(email) == None:
        raise ValidationError(
            'Email is not valid.', code='not_valid_email'
        )
