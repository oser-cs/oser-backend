"""Users models."""


from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as _UserManager

from users.utils import get_promotion_range
from utils import modify_fields

# Create your models here.


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
    first_name={'blank': False},
    last_name={'blank': False},
)
class User(AbstractUser):
    """Django Contrib user. For possible future refinements only.

    Fields
    ----------
    date_of_birth : date
    gender : char (choices: 'M' or 'F')
    phone_number : char
    """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    date_of_birth = models.DateField('date de naissance',
                                     blank=False, null=True)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Homme'),
        (FEMALE, 'Femme'),
    )
    gender = models.CharField('sexe',
                              max_length=1, choices=GENDER_CHOICES,
                              default=MALE)

    # TODO add a proper phone number validator
    phone_number = models.CharField('téléphone',
                                    max_length=12, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('api:user-detail', args=[str(self.id)])


class Tutor(models.Model):
    """Represents a tutor.

    Fields
    ------
    user : 1-1 with User
    promotion : int
    """

    user = models.OneToOneField('User', on_delete=models.CASCADE)
    PROMOTION_CHOICES = tuple(
        (year, str(year)) for year in get_promotion_range()
    )
    promotion = models.IntegerField(choices=PROMOTION_CHOICES,
                                    default=PROMOTION_CHOICES[0][0])

    class Meta:  # noqa
        verbose_name = 'tuteur'

    def __str__(self):
        return str(self.user)
