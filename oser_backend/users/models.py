"""Users models."""

from django.contrib.auth.models import UserManager as _UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from dry_rest_permissions.generics import authenticated_users

from users.utils import get_promotion_range
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

    Fields
    ----------
    date_of_birth : date
    gender : char (choices: 'M' or 'F')
    phone_number : char
    profile_type : char
    """

    USERNAME_FIELD = 'email'  # default was: username

    # v List of fields prompted when creating a superuser
    REQUIRED_FIELDS = ['first_name', 'last_name']  # removed email

    objects = UserManager()

    date_of_birth = models.DateField(blank=True, null=True,
                                     verbose_name='date de naissance')

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Homme'),
        (FEMALE, 'Femme'),
    )
    gender = models.CharField('sexe', blank=True, null=True,
                              max_length=1, choices=GENDER_CHOICES)

    # TODO add a proper phone number validator
    phone_number = models.CharField('téléphone',
                                    max_length=20, null=True, blank=True)

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


# Define user profiles here.


class ProfileMixin:

    def __str__(self):
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        return f'{self.__class__.__name__} {self.pk}'

    def get_absolute_url(self):
        return reverse(self.detail_view_name, args=[self.pk])

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True


class Student(ProfileMixin, models.Model):
    """Represents a student profile."""

    detail_view_name = 'api:student-detail'

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='utilisateur',
        related_name='student')

    address = models.ForeignKey(
        'core.Address',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='adresse')

    tutoring_group = models.ForeignKey(
        'tutoring.TutoringGroup',
        on_delete=models.SET_NULL,
        null=True,
        related_name='students',
        verbose_name='groupe de tutorat')

    school = models.ForeignKey(
        'tutoring.School',
        on_delete=models.SET_NULL,
        null=True,
        related_name='students',
        verbose_name='lycée')

    class Meta:  # noqa
        verbose_name = 'lycéen'


class Tutor(ProfileMixin, models.Model):
    """Represents a tutor profile."""

    detail_view_name = 'api:tutor-detail'

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='utilisateur',
        related_name='tutor')

    PROMOTION_CHOICES = tuple(
        (year, str(year)) for year in get_promotion_range()
    )
    promotion = models.IntegerField(choices=PROMOTION_CHOICES,
                                    default=PROMOTION_CHOICES[0][0])

    class Meta:  # noqa
        verbose_name = 'tuteur'
