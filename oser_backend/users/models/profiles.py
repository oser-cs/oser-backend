"""User profiles models."""

from django.apps import apps
from django.db import models
from django.shortcuts import reverse
from dry_rest_permissions.generics import (allow_staff_or_superuser,
                                           authenticated_users)

from ..apps import UsersConfig
from ..utils import get_promotion_range


# Generic profile


def get_profile_type(model):
    return model._meta.model_name


def get_natural_profile_type(model):
    return model._meta.verbose_name.capitalize()


class ProfileMeta(models.base.ModelBase):
    """Extended metaclass for the Profile model.

    Allows to dynamically create the choices for the UserAccount.profile_type
    field.

    Attributes
    ----------
    PROFILE_TYPES : list of 2-tuples
        Directly usable by a field "choices" option.
    """

    PROFILE_TYPES = []

    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        if name != 'Profile':  # don't add the base profile model
            profile_type = get_profile_type(cls)
            natural = get_natural_profile_type(cls)
            metacls.PROFILE_TYPES.append(
                (profile_type, natural))
        return cls


class Profile(models.Model, metaclass=ProfileMeta):
    """Generic profile model.

    In 1-1 relationship with User:
        profile = user.profile  # profile from user
        user = profile.user  # user from profile

    Define a specific profile by subclassing this model and defining more
    model fields.

    Attributes
    ----------
    detail_view_name : str
        Must be set on concrete profiles.
        If not set, calling get_absolute_url() will raise an AttributeError.
    """

    user = models.OneToOneField('users.User',
                                on_delete=models.CASCADE,
                                verbose_name='utilisateur',
                                primary_key=True,
                                related_name='profile_object')
    detail_view_name = None

    class Meta:  # noqa
        verbose_name = 'profil'
        ordering = ['user__last_name', 'user__first_name']

    @property
    def id(self):
        return self.user_id

    @property
    def full_name(self):
        return self.user.get_full_name()

    @classmethod
    def get_profile_type_choices(cls):
        """Return the available profile types.

        Returns
        -------
        profile_types : tuple of 2-tuples
            Directly usable by a choices field option.
        """
        return tuple(type(cls).PROFILE_TYPES)

    @classmethod
    def get_model(cls, profile_type):
        """Return the Django model associated with a profile type.

        Raises
        ------
        ValueError :
            If profile_type is not associated with a profile model.
        """
        model = apps.get_model(UsersConfig.name, profile_type)
        return model

    def get_absolute_url(self):
        """Return the profile's absolute url.

        The absolute url is obtained by reversing detail_view_name and
        passing the profile's primary key as argument.

        Raises
        ------
        AttributeError :
            If detail_view_name is not set on the model.
        """
        if self.detail_view_name is None:
            raise AttributeError('detail_view_name must be set on {}'
                                 .format(self.__class__))
        return reverse(self.detail_view_name, args=[str(self.pk)])

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        """Only authenticated users can read profile of other users."""
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        """Only authenticated can read profile of another user."""
        return True

    @staticmethod
    def has_write_permission(request):
        """Allow anyone to create new profile through registration."""
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        """Only owners of the profile can update/delete it."""
        return request.user.id == self.user.id

    def __str__(self):
        return str(self.full_name)


# Define user profiles here.

class Student(Profile):
    """Represents a student profile.

    Fields
    ------
    address : char  # TODO update when validated address field implemented
    tutoring_group : 1-n with tutoring.TutoringGroup
        Deletion rule: SET_NULL
    school : 1-n with tutoring.School
        Deletion rule: SET_NULL
    """

    detail_view_name = 'api:student-detail'
    # TODO convert to validated address field
    address = models.CharField('adresse', max_length=200)

    tutoring_group = models.ForeignKey('tutoring.TutoringGroup',
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       related_name='students')
    school = models.ForeignKey('tutoring.School',
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='students')

    class Meta:  # noqa
        verbose_name = 'lycéen'


class Tutor(Profile):
    """Represents a tutor profile.

    Fields
    ------
    promotion : int
    tutoring_groups : n-n with TutoringGroup
    """

    detail_view_name = 'api:tutor-detail'
    PROMOTION_CHOICES = tuple(
        (year, str(year)) for year in get_promotion_range()
    )
    promotion = models.IntegerField(choices=PROMOTION_CHOICES,
                                    default=PROMOTION_CHOICES[0][0])

    class Meta:  # noqa
        verbose_name = 'tuteur'


class SchoolStaffMember(Profile):
    """Represents a member of a school's staff.

    Fields
    ------
    school : 1-n with tutoring.School
        Deletion rule: CASCADE
    role : char
        The person's role in the school.
    """

    detail_view_name = 'api:schoolstaffmember-detail'
    school = models.ForeignKey('tutoring.School', on_delete=models.CASCADE,
                               verbose_name='lycée',
                               related_name='staffmembers')
    role = models.CharField('rôle', max_length=100)

    class Meta:  # noqa
        verbose_name = 'membre du personnel de lycée'
        verbose_name_plural = 'membres du personnel de lycée'
