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

    registration = models.OneToOneField(
        'register.Registration',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="dossier d'inscription",
        related_name='student',
    )

    gender = models.CharField(max_length=20,
        null=True,
        blank=True,
        verbose_name="genre",
    )

    addressNumber = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="numéro de rue"
    )

    street = models.CharField(max_length=70,
        null=True,
        blank=True,
        verbose_name="nom de rue"
    )

    city = models.CharField(max_length=50,
        null=True,
        blank=True,
        verbose_name="nom de ville"
    )

    personnalPhone = models.CharField(max_length=12,
        null=True,
        blank=True,
        verbose_name="numéro de téléphone personnel"
    )

    parentsPhone = models.CharField(max_length=12,
        null=True,
        blank=True,
        verbose_name="numéro de téléphone parental"
    )

    parentsEmail = models.EmailField(max_length=20,
        null=True,
        blank=True,
        verbose_name="adresse mail parentale"
    )


    school = models.CharField(max_length=70,
        null=True,
        blank=True,
        verbose_name="nom de l'école"
    )


    grade = models.CharField(max_length=20,
        null=True,
        blank=True,
        verbose_name="niveau de la classe"
    )


    scholarship = models.NullBooleanField(
        null=True,
        blank=True,
        verbose_name="boursier"
    )


    fatherActivity = models.CharField(max_length=70,
        null=True,
        blank=True,
        verbose_name="métier du père"
    )


    motherActivity = models.CharField(max_length=70,
        null=True,
        blank=True,
        verbose_name="métier de la mère"
    )


    parentsStatus = models.CharField(max_length=30,
        null=True,
        blank=True,
        verbose_name="statut des parents"
    )


    dependantsNumber = models.CharField(max_length=12,
        null=True,
        blank=True,
        verbose_name="numéro d'urgence"
    )

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True


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

    address = models.OneToOneField(
        'core.Address',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='adresse',
        related_name='tutor')

    PROMOTION_CHOICES = tuple(
        (year, str(year)) for year in get_promotion_range()
    )
    promotion = models.IntegerField(choices=PROMOTION_CHOICES,
                                    default=PROMOTION_CHOICES[0][0])

    class Meta:  # noqa
        verbose_name = 'tuteur'
