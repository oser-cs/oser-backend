"""Visits models."""
from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import now
from dry_rest_permissions.generics import authenticated_users

from markdownx.models import MarkdownxField


class VisitQuerySet(models.QuerySet):
    """Custom Visit queryset."""

    def registrations_open(self, open: bool):
        """Filter visits whose registrations are open or closed.

        Equivalent to: queryset.filter(registrations_open=open)
        (Django does not allow this syntax because
        registrations_open is a property.)

        open : bool
            True corresponds to open registrations,
            False to closed registrations.
        """
        today = now()
        if open:
            return self.filter(deadline__gte=today)
        else:
            return self.filter(deadline__lt=today)

    def passed(self):
        """Return a queryset containing only passed visits.

        A visit is passed if its date is strictly after today.
        """
        return self.filter(date__gt=now().date())


class Participation(models.Model):
    """Represents the participation of a user to a visit.

    Allows to store whether the user was present to the visit,
    and whether their files were validated.
    """

    user = models.ForeignKey('users.User', verbose_name='utilisateur',
                             related_name='participations',
                             on_delete=models.CASCADE, null=True)
    visit = models.ForeignKey('Visit', verbose_name='sortie',
                              related_name='participations',
                              on_delete=models.CASCADE)
    accepted = models.NullBooleanField(
        'accepté',
        help_text=(
            "Cocher pour confirmer au tutoré sa participation à la sortie."))
    present = models.NullBooleanField(
        'présent',
        help_text=(
            "Une fois la sortie passée, indiquer si le lycéen était présent."
        )
    )

    class Meta:  # noqa
        verbose_name = 'participation'
        # prevent a user from participating visit multiple times
        unique_together = (('user', 'visit'),)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.accepted is not None:
            self.notify_participation()

    def notify_participation(self):
        if self.accepted is True:
            from .notifications import Accepted
            Accepted(user=self.user, visit=self.visit).send()
        elif self.accepted is False:
            from .notifications import Rejected
            Rejected(user=self.user, visit=self.visit).send()

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


class VisitOrganizer(models.Model):
    """Represent a tutor who organizes a visit."""

    tutor = models.ForeignKey(
        'profiles.Tutor', on_delete=models.CASCADE, verbose_name='tuteur')
    visit = models.ForeignKey(
        'Visit', on_delete=models.CASCADE, verbose_name='sortie')

    class Meta:  # noqa
        verbose_name = 'organisateur'

    def __str__(self):
        return str(self.tutor)


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
        help_text=('Une description plus complète des activités proposées '
                   'durant la sortie. Ce champ supporte Markdown.'))
    place = models.ForeignKey(
        'Place',
        verbose_name='lieu',
        on_delete=models.SET_NULL,
        null=True)
    date = models.DateField(
        help_text="Date de la sortie.")
    start_time = models.TimeField(
        'heure de début',
        help_text='Heure de début de la sortie. Format : hh:mm.')
    end_time = models.TimeField(
        'heure de fin',
        help_text='Heure de fin de la sortie. Format : hh:mm.')
    meeting = models.CharField(
        'lieu de rendez-vous',
        max_length=100, blank=True, default='',
        help_text=('Indiquez aux tutorés où ils devront vous retrouver. '
                   'Exemple : "devant le musée".'))
    deadline = models.DateTimeField(
        "date limite d'inscription",
        help_text=("Note : les lycéens ne pourront plus s'inscrire "
                   "passée cette date. Format de l'heure : hh:mm."))
    image = models.ImageField(
        'illustration',
        blank=True, null=True,
        help_text='Une illustration représentative de la sortie.',
        upload_to='visits/images/')
    fact_sheet = models.FileField(
        'fiche sortie', blank=True, null=True,
        upload_to='visits/fact_sheets/',
        help_text=('Informe le lycéen de détails sur la sortie. '
                   'Tous formats supportés, PDF recommandé.'))
    permission = models.FileField(
        'autorisation de sortie', blank=True, null=True,
        upload_to='visits/visit_permissions/',
        help_text=('À mettre à disposition pour que le lycéen la remplisse. '
                   'Tout format supporté, PDF recommandé.'))
    participants = models.ManyToManyField('users.User',
                                          through='Participation')
    organizers = models.ManyToManyField('profiles.Tutor',
                                        through='VisitOrganizer',
                                        related_name='organized_visits')

    def _registrations_open(self):
        return now() < self.deadline
    # display fancy icon in admin instead of True/False
    _registrations_open.boolean = True
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

    @staticmethod
    @authenticated_users
    def has_write_permission(request):
        return True

    @authenticated_users
    def has_object_write_permission(self, request):
        return True

    def get_absolute_url(self):
        return reverse('api:visit-detail', args=[str(self.pk)])

    def get_site_url(self):
        return f'http://oser-cs.fr/visits/{self.pk}'

    def __str__(self):
        return str(self.title)


class Place(models.Model):
    """Represents a place a visit happens at."""

    name = models.CharField('nom', max_length=200)
    address = models.ForeignKey(
        'core.Address', on_delete=models.CASCADE, null=True,
        verbose_name='adresse',
        help_text='Adresse complète de ce lieu'
    )
    description = MarkdownxField(
        default='', blank=True,
        help_text=(
            "Une description de ce lieu : de quoi s'agit-il ? "
            "Ce champ supporte Markdown."
        )
    )

    class Meta:  # noqa
        verbose_name = 'lieu'
        verbose_name_plural = 'lieux'
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('api:place-detail', args=[str(self.pk)])

    def __str__(self):
        return str(self.name)
