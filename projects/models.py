"""Projects models."""

from django.db import models
from django.utils import timezone

from markdownx.models import MarkdownxField


class Project(models.Model):
    """Represents a project that can have multiple editions over the years."""

    name = models.CharField(
        'nom', max_length=200,
        help_text='Le nom du projet.')

    description = MarkdownxField(
        help_text='Une description générale du projet')

    logo = models.ImageField(
        null=True, blank=True, upload_to='projects/logos/',
        help_text='Le logo du projet ou une image représentative.')

    editions: models.Manager

    class Meta:  # noqa
        verbose_name = 'projet'
        ordering = ('name',)

    def __str__(self):
        return str(self.name)


def this_year() -> int:
    """Return the current year."""
    return timezone.now().year()


class Edition(models.Model):
    """Represents an instance of a project for a given year."""

    name = models.CharField(
        'nom', max_length=200, default='', blank=True,
        help_text='Un nom optionnel pour cette édition (exemple : "Berlin").')

    year = models.IntegerField(
        'année', default=this_year,
        help_text="L'année où se déroule cette édition.")

    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE,
        verbose_name='projet', related_name='editions',
        help_text='Le projet dont ceci est une édition.')

    description = MarkdownxField(
        help_text=(
            'Une description spécifique pour cette édition.'
        ))

    organizers = models.ManyToManyField(
        'users.User', through='EditionOrganizer')

    participations: models.Manager

    class Meta:  # noqa
        ordering = ('-year',)
        verbose_name = 'édition'

    def __str__(self) -> str:
        """Represent using the project name, the year and the edition name."""
        s = f'{self.project} édition {self.year}'
        if self.name:
            s += f' ({self.name})'
        return s


class Participation(models.Model):
    """Represents the participation of a user (a student) to a project."""

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, verbose_name='utilisateur',
        related_name='project_participations')

    edition = models.ForeignKey(
        'Edition', on_delete=models.CASCADE, verbose_name='sortie',
        related_name='participations')

    submitted = models.DateTimeField(
        auto_now_add=True, verbose_name='soumis le',
        help_text='Date de soumission de la participation')

    STATUS_PENDING = 'pending'
    STATUS_VALIDATED = 'valid'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_CANCELLED = 'cancelled'
    _STATUS_CHOICES = (
        (STATUS_PENDING, 'En attente'),
        (STATUS_VALIDATED, 'Validé'),
        (STATUS_ACCEPTED, 'Accepté'),
        (STATUS_REJECTED, 'Refusé'),
        (STATUS_CANCELLED, 'Annulé'),
    )
    status = models.CharField(
        'statut', max_length=10, choices=_STATUS_CHOICES,
        help_text=(
            "L'état de la participation. "
            "En attente = en cours de validation par les organisateurs. "
            "Validé = toutes les pièces ont été reçues et sont conformes. "
            "Accepté = le lycéen a été sélectionné pour participer. "
            "Refusé = le lycéen n'a pas été sélectionné pour participer. "
            "Annulé = le lycéen a annulé sa participation."
        ))

    class Meta:  # noqa
        ordering = ('-submitted',)

    def __str__(self):
        return str(self.user)


class EditionOrganizer(models.Model):
    """Represents a user (a tutor) who organizes an edition of a project."""

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, verbose_name='utilisateur')
    edition = models.ForeignKey(
        'Edition', on_delete=models.CASCADE, verbose_name='édition')

    class Meta:  # noqa
        verbose_name = 'organisateur'

    def __str__(self):
        return str(self.user)
