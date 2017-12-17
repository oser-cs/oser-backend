"""User profiles models."""

from django.db import models
from django.apps import apps
from django.shortcuts import reverse
from ..utils import get_promotion_range
from ..apps import UsersConfig


# Generic profile

class ProfileMeta(models.base.ModelBase):
    """Extended metaclass for the Profile model.

    Allows to dynamically create the choices for the UserAccount.profile_type
    field.
    """

    PROFILE_TYPES = []

    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        if name != 'Profile':
            metacls.PROFILE_TYPES.append((
                name.lower(),
                cls._meta.verbose_name.capitalize()
            ))
        return cls


class Profile(models.Model, metaclass=ProfileMeta):
    """Generic profile model.

    In 1-1 relationship with User:
        profile = user.profile  # profile from user
        user = profile.user  # user from profile

    Generic fields defined here
    ---------------------------
    phone_number : char
    date_of_birth : date

    Define a specific profile by subclassing this model and defining more
    model fields.
    """

    user = models.OneToOneField('users.User',
                                on_delete=models.CASCADE,
                                verbose_name='utilisateur',
                                primary_key=True,
                                related_name='profile_object')
    phone_number = models.CharField(max_length=12, null=True, blank=True,
                                    verbose_name='téléphone')
    date_of_birth = models.DateField(null=True,
                                     verbose_name='date de naissance')

    class Meta:  # noqa
        verbose_name = 'profil'
        ordering = ['user__last_name', 'user__first_name']

    @property
    def id(self):
        return self.user_id

    @classmethod
    def get_profile_types(cls):
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

    @property
    def full_name(self):
        return self.user.get_full_name()

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

    def get_absolute_url(self):
        return reverse('api:student-detail', args=[str(self.id)])


class Tutor(Profile):
    """Represents a tutor profile.

    Fields
    ------
    promotion : int
    tutoring_groups : n-n with TutoringGroup
    """

    PROMOTION_CHOICES = tuple(
        (year, str(year)) for year in get_promotion_range()
    )
    promotion = models.IntegerField(choices=PROMOTION_CHOICES,
                                    default=PROMOTION_CHOICES[0][0])

    class Meta:  # noqa
        verbose_name = 'tuteur'

    def get_absolute_url(self):
        return reverse('api:tutor-detail', args=[str(self.id)])


class SchoolStaffMember(Profile):
    """Represents a member of a school's staff.

    Fields
    ------
    school : 1-n with tutoring.School
        Deletion rule: CASCADE
    role : char
        The person's role in the school.
    """

    school = models.ForeignKey('tutoring.School', on_delete=models.CASCADE,
                               verbose_name='lycée',
                               related_name='staffmembers')
    role = models.CharField('rôle', max_length=100)

    class Meta:  # noqa
        verbose_name = 'personnel de lycée'
        verbose_name_plural = 'personnels de lycée'

    def get_absolute_url(self):
        return reverse('api:schoolstaffmember-detail', args=[str(self.id)])
