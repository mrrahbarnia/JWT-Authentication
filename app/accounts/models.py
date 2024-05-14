from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models  import PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(
            self, email: str, is_active: bool = True, is_staff: bool = False, password: str | None = None
    ):
        if not email:
            raise ValueError('Users must have an email address...')

        user: AbstractBaseUser = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active, is_staff=is_staff
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str | None = None):
        user: AbstractBaseUser = self.create_user(
            email=email,
            is_active=True,
            is_staff=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    Roles = [
        ('AD', 'Admin'),
        ('NU', 'Normal User')
    ]

    email = models.EmailField(verbose_name='Email address', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=2, choices=Roles, default='NU')

    objects = UserManager()

    USERNAME_FIELD = 'email'

