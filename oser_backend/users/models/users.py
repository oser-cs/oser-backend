"""Users models."""
from django.contrib.auth.models import UserManager as _UserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import reverse
from dry_rest_permissions.generics import authenticated_users

from utils import modify_fields

from .profiles import Profile


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
        The type of profile this user has. Used to polymorphically find
        the profile corresponding to a user (profiles can be of various
        types) through user.profile.
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
    # allows to access the Profile object through user.profile
    profile_type = models.CharField(max_length=20,
                                    null=True,
                                    choices=Profile.get_profile_type_choices(),
                                    verbose_name='type de profil')

    @property
    def profile(self):
        """Return the profile of the user.

        The returned object is an instance of the model corresponding to
        the profile_type.

        Example: if profile_type is 'student', user.profile will be a
        Student object.
        """
        return self.profile_object
        # if not self.profile_type:
        #     raise AttributeError('User has no profile')
        # model = Profile.get_model(self.profile_type)
        # return model.objects.get(user_id=self.id)
    profile.fget.short_description = 'profil'

    def get_absolute_url(self):
        return reverse('api:user-detail', args=[str(self.id)])

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        """Anyone can create a user."""
        return True

    @authenticated_users
    def has_object_write_permission(self, request):
        return request.user.id == self.id
