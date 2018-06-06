"""Profiles models."""

from django.db import models
from django.shortcuts import reverse
from dry_rest_permissions.generics import authenticated_users
from .utils import get_promotion_range


class ProfileMixin:
    """Mixin with common functionnality for profiles."""

    detail_view_name = None

    def __str__(self):
        """Represent with full name or email."""
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        return self.user.email

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

    tutoring_group = models.ForeignKey(
        'tutoring.TutoringGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='groupe de tutorat')

    school = models.ForeignKey(
        'tutoring.School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='lycée')

    registration = models.OneToOneField(
        'register.Registration',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="dossier d'inscription",
        related_name='student',
    )

    @property
    def address(self):
        """Address of the student defined in their registration."""
        return getattr(self.registration, 'address', None)

    @property
    def emergency_contact(self):
        """Emergency contact of the student defined in their registration."""
        return getattr(self.registration, 'emergency_contact', None)

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
