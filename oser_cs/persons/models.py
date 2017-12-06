"""Persons models."""

from django.db import models
from django.contrib.auth import get_user_model
from persons.utils import get_promotion_range

# Create your models here.


# TODO define the abstract Person model
class Person:
    """Represents a person who can use the website."""


class Tutor(models.Model):
    """Represents a tutor.

    Fields
    ------
    user : 1-1 with User
        Deleting the user will delete the tutor too (delete cascade).
    promotion : int
    tutoring_groups : 1-n with TutoringGroup
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    PROMOTION_CHOICES = tuple(
        (year, str(year)) for year in get_promotion_range()
    )
    promotion = models.IntegerField(choices=PROMOTION_CHOICES,
                                    default=PROMOTION_CHOICES[0][0])

    class Meta:  # noqa
        verbose_name = 'tuteur'

    def __str__(self):
        return str(self.user)
