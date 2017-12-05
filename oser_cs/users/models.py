"""Users models."""

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager

from utils import modify_fields

# Create your models here.


class UserManager(_UserManager):
    """Custom user manager.

    Makes email mendatory instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with email and password."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


@modify_fields(
    username={'blank': True, '_unique': False},
    email={'_unique': True, 'blank': False},
    first_name={'blank': False},
    last_name={'blank': False},
)
class User(AbstractUser):
    """Django Contrib user. For possible future refinements only.

    Fields
    ----------
    phone_number : char field
    """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = UserManager()

    date_of_birth = models.DateField('date de naissance', null=True)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'masculin'),
        (FEMALE, 'féminin'),
    )
    gender = models.CharField('sexe',
                              max_length=1, choices=GENDER_CHOICES,
                              default=MALE)

    # TODO add a proper phone number validator
    phone_number = models.CharField('téléphone',
                                    max_length=12, blank=True)

    def get_absolute_url(self):
        return reverse('api:user-detail', args=[str(self.id)])
