"""Persons models."""

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from persons.utils import get_promotion_range

# Create your models here.


class Person(models.Model):
    """Represents a person who can use the website.

    Abstract model.

    Fields
    ------
    user : 1-1 with User
        Deletion rule: CASCADE

    Properties
    ----------
    full_name : str
        Alias to user.get_full_name()

    Meta
    ----
    ordering : by last name, by first name
    """

    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name='utilisateur',
                                null=True)

    @property
    def full_name(self):
        return self.user.get_full_name()

    class Meta:  # noqa
        abstract = True
        verbose_name = 'personne'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return str(self.full_name)


class Student(Person):
    """Represents a student.

    Inherits from the Person abstract model.

    Fields
    ------
    address : char  # TODO update when validated address field implemented
    tutoring_group : 1-n with tutoring.TutoringGroup
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


class Tutor(Person):
    """Represents a tutor.

    Inherits from the Person abstract model.

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


class SchoolStaffMember(Person):
    """Represents a member of a school's staff.

    Inherits from the Person abstract model.

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
