"""Users models."""

from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """Django Contrib user. For possible future refinements only.

    Fields
    ----------
    phone_number : char field

    """

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'masculin'),
        (FEMALE, 'féminin'),
    )
    gender = models.CharField('sexe',
                              max_length=1, choices=GENDER_CHOICES)

    # TODO add a proper phone number validator
    phone_number = models.CharField('téléphone',
                                    max_length=12, blank=True)

    def get_absolute_url(self):
        return reverse('users:user-detail', args=[str(self.id)])
