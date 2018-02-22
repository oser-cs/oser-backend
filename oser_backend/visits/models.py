"""Visits models."""
import pytz
from django.utils import timezone
from django.db import models
from django.shortcuts import reverse
from dry_rest_permissions.generics import authenticated_users
from markdownx.models import MarkdownxField

utc = pytz.UTC

# Create your models here.


class VisitQuerySet(models.QuerySet):
    """Custom Visit queryset.

    Allow filtering by whether registrations are open or closed.
    """

    def registrations_open(self, state):
        """Filter visits whose registrations are open or closed.

        Equivalent to: queryset.filter(registrations_open=state)
        (Django does not allow this syntax because
        registrations_open is a property.)

        state : boolean
            True corresponds to open registrations,
            False to closed registrations.
        """
        now = timezone.now()
        if state:
            return self.filter(deadline__gte=now)
        else:
            return self.filter(deadline__lt=now)


class Visit(models.Model):
    """Represents a visit that students can attend."""

    objects = VisitQuerySet.as_manager()

    title = models.CharField(
        'titre', max_length=100,
        help_text=(
            "Préciser si besoin le type de sortie (exposition, concert…) "
        ))
    summary = models.CharField(
        'résumé', max_length=300,
        default='', blank=True,
        help_text=(
            "Une ou deux phrases décrivant la sortie de manière attrayante."
        ))
    description = MarkdownxField(
        blank=True, default='',
        help_text=(
            "Une description plus complète des activités proposées durant "
            "la sortie. Ce champ supporte Markdown."
        ))
    # TODO Place model
    place = models.CharField(
        'lieu', max_length=100,
        help_text=(
            "Indiquer simplement le nom du lieu où se déroule la "
            "sortie. L'adresse exacte de rendez-vous devrait plutôt"
            "être précisé dans la fiche sortie."
        ))
    date = models.DateTimeField(
        help_text="Heure de début de la sortie. Format de l'heure : hh:mm.")
    deadline = models.DateTimeField(
        "date limite d'inscription",
        help_text=(
            "Note : les lycéens ne pourront plus s'inscrire "
            "passé cette date. Format de l'heure : hh:mm."
        ))
    image = models.ImageField(
        'illustration',
        blank=True, null=True,
        help_text=(
            "Une illustration représentative de la sortie. "
            "Dimensions : ???x???"
        ))
    fact_sheet = models.FileField(
        'fiche sortie', blank=True, null=True,
        help_text="Formats supportés : PDF")

    def _registrations_open(self):
        return timezone.now() < self.deadline
    # to display fancy icon instead of True/False
    _registrations_open.boolean = True
    # don't define property directly because prop.fget.boolean doesn't work
    registrations_open = property(_registrations_open)
    registrations_open.fget.short_description = 'Inscriptions ouvertes'

    class Meta:  # noqa
        ordering = ('date',)
        verbose_name = 'sortie'

    # Read-only permissions

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    def get_absolute_url(self):
        return reverse('api:visit-detail', args=[str(self.pk)])

    def __str__(self):
        return str(self.title)
