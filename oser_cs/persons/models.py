"""Persons models."""

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from persons.utils import get_promotion_range

# Create your models here.


# TODO define the abstract Person model
class Person:
    """Represents a person who can use the website."""


class Student(models.Model):
    """Represents a student.

    Fields
    ------
    user : 1-1 with User
        Deletion rule: CASCADE
    address : char  # TODO update when validated address field implemented
    tutoring_group : 1-n with TutoringGroup
        Deletion rule: SET_NULL
    """

    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name='utilisateur',
                                null=True)

    # TODO convert to validated address field
    address = models.CharField('adresse', max_length=200)

    tutoring_group = models.ForeignKey('tutoring.TutoringGroup',
                                       on_delete=models.SET_NULL,
                                       null=True)

    def get_absolute_url(self):
        return reverse('api:student-detail', args=[str(self.id)])


class Tutor(models.Model):
    """Represents a tutor.

    Fields
    ------
    user : 1-1 with User
        Deletion rule: CASCADE
    promotion : int
    tutoring_groups : n-n with TutoringGroup
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    PROMOTION_CHOICES = tuple(
        (year, str(year)) for year in get_promotion_range()
    )
    promotion = models.IntegerField(choices=PROMOTION_CHOICES,
                                    default=PROMOTION_CHOICES[0][0])

    class Meta:  # noqa
        verbose_name = 'tuteur'

    def get_absolute_url(self):
        return reverse('api:tutor-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.user)
