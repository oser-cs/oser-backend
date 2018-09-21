"""Users models.

Redefinition of Django user managers to use email authentication.
"""

from django.contrib.auth.models import UserManager as _UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from dry_rest_permissions.generics import authenticated_users
from utils import modify_fields


class UserManager(_UserManager):
    """Custom user manager.

    Makes email mandatory instead of username.
    """

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with email and password."""
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


@modify_fields(
    username={'blank': True, '_unique': False, 'null': True},
    email={'_unique': True, 'blank': False, 'null': False},
)
class User(AbstractUser):
    """Custom user.

    User identification happens by email and password.
    """

    USERNAME_FIELD = 'email'  # default was: username

    # v List of fields prompted when creating a superuser
    REQUIRED_FIELDS = ['first_name', 'last_name']  # removed email

    objects = UserManager()

    # type of profile of the user
    PROFILE_STUDENT = 0
    PROFILE_TUTOR = 1
    PROFILE_CHOICES = (
        (PROFILE_STUDENT, 'Lycéen'),
        (PROFILE_TUTOR, 'Tuteur'),
    )
    profile_type = models.CharField(max_length=20,
                                    null=True,
                                    choices=PROFILE_CHOICES,
                                    verbose_name='type de profil')

    phone_number = models.CharField('téléphone',
                                    max_length=20, null=True, blank=True)

    @property
    def student(self):
        return getattr(self, 'student', None)
    student.fget.short_description = 'profil lycéen'

    @property
    def tutor(self):
        return getattr(self, 'tutor', None)
    tutor.fget.short_description = 'profil tuteur'

    def get_absolute_url(self):
        return reverse('api:user-detail', args=[str(self.id)])

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True
