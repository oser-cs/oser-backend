"""Visits models."""
import pytz
from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import now
from dry_rest_permissions.generics import authenticated_users
from markdownx.models import MarkdownxField

utc = pytz.UTC

# Create your models here.


class VisitQuerySet(models.QuerySet):
    """Custom Visit queryset."""

    def registrations_open(self, state):
        """Filter visits whose registrations are open or closed.

        Equivalent to: queryset.filter(registrations_open=state)
        (Django does not allow this syntax because
        registrations_open is a property.)

        state : boolean
            True corresponds to open registrations,
            False to closed registrations.
        """
        today = now()
        if state:
            return self.filter(deadline__gte=today)
        else:
            return self.filter(deadline__lt=today)

    def passed(self):
        """Return a queryset containing only passed visits.

        A visit is passed if its date is strictly after today.
        """
        return self.filter(date__gt=now())


class VisitParticipant(models.Model):
    """Through-model for visit participants.

    Allows to store whether the user was present to the visit.
    """

    user = models.ForeignKey('users.User', verbose_name='utilisateur',
                             on_delete=models.CASCADE, null=True)
    visit = models.ForeignKey('Visit', verbose_name='sortie',
                              on_delete=models.CASCADE)
    present = models.NullBooleanField('présent')

    class Meta:  # noqa
        verbose_name = 'participant à la sortie'
        verbose_name_plural = 'participants à la sortie'
        # prevent a user from participating visit multiple times
        unique_together = (('user', 'visit'),)

    def get_absolute_url(self):
        return reverse('api:visit-participants-detail', args=[str(self.pk)])

    # Permissions

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    @authenticated_users
    def has_object_write_permission(self, request):
        return True

    def __str__(self):
        return '{} participates in {}'.format(self.user, self.visit)


class Visit(models.Model):
    """Represents a visit that users can attend."""

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
    place = models.ForeignKey(
        'Place',
        verbose_name='lieu',
        on_delete=models.SET_NULL,
        null=True)
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
    participants = models.ManyToManyField('users.User',
                                          through='VisitParticipant')
    organizers_group = models.OneToOneField('auth.Group',
                                            on_delete=models.SET_NULL,
                                            null=True,
                                            verbose_name='organisateurs')

    def _registrations_open(self):
        return now() < self.deadline
    # to display fancy icon instead of True/False
    _registrations_open.boolean = True
    # don't define property directly because prop.fget.boolean doesn't work
    registrations_open = property(_registrations_open)
    registrations_open.fget.short_description = 'Inscriptions ouvertes'

    @property
    def organizers_group_name(self):
        return 'Organisateurs - {} : {}'.format(self.id, self.title)

    class Meta:  # noqa
        ordering = ('date',)
        verbose_name = 'sortie'
        permissions = (
            ('manage_visit', 'Can manage visit'),
        )

    # Read-only permissions

    @staticmethod
    @authenticated_users
    def has_read_permission(request):
        return True

    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    @authenticated_users
    def has_object_write_permission(self, request):
        return True

    def get_absolute_url(self):
        return reverse('api:visit-detail', args=[str(self.pk)])

    def __str__(self):
        return str(self.title)


class Place(models.Model):
    """Represents a place a visit happens at."""

    name = models.CharField('nom', max_length=200)
    address = models.CharField(
        'adresse', max_length=200,
        help_text=(
            "L'adresse complète de ce lieu : "
            "numéro, rue ou voie, code postal, ville, pays si pertinent."
        ))
    description = MarkdownxField(
        default='', blank=True,
        help_text=(
            "Une description de ce lieu : de quoi s'agit-il ? "
            "Ce champ supporte Markdown."
        ))

    class Meta:  # noqa
        verbose_name = 'lieu'
        verbose_name_plural = 'lieux'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('api:place-detail', args=[str(self.pk)])

    def __str__(self):
        return str(self.name)
