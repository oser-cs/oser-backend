"""Projects models."""

from django.db import models
from django.core.validators import ValidationError

from markdownx.models import MarkdownxField

from profiles.models import Tutor
from .utils import this_year


class Project(models.Model):
    """Represents a project that can have multiple editions over the years."""

    name = models.CharField(
        'nom', max_length=200,
        help_text='Le nom du projet.')

    description = MarkdownxField(
        blank=True, default='',
        help_text='Une description générale du projet')

    logo = models.ImageField(
        null=True, blank=True, upload_to='projects/logos/',
        help_text='Le logo du projet ou une image représentative.')

    editions: models.Manager

    class Meta:  # noqa
        verbose_name = 'projet'
        ordering = ('name',)

    def total_participations(self, state: str=None) -> int:
        """Return the total number of accepted participations for this project.

        Parameters
        ----------
        state : str, optional
            If passed, only the participations in this state will be counted.

        """
        state = state or Participation.STATE_ACCEPTED
        filter = models.Q(participations__state=state)
        return self.editions.aggregate(
            t=models.Count('participations', filter=filter)
        )['t']

    def __str__(self) -> str:
        """Represent by its name."""
        return str(self.name)


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
        blank=True, default='',
        help_text=(
            'Une description spécifique pour cette édition.'
        ))

    organizers = models.ManyToManyField(
        'users.User', through='EditionOrganizer')

    participations: models.Manager

    class Meta:  # noqa
        ordering = ('-year',)
        verbose_name = 'édition'
        get_latest_by = 'year'

    def __str__(self) -> str:
        """Represent using the project name, the year and the edition name."""
        s = f'{self.project} édition {self.year}'
        if self.name:
            s += f' ({self.name})'
        return s


def _validate_address_is_set(recipient_id: int):
    recipient = Tutor.objects.filter(pk=recipient_id).first()
    if recipient and not recipient.address:
        raise ValidationError("Le destinataire doit avoir une adresse.")


validate_address_is_set = _validate_address_is_set


class EditionForm(models.Model):
    """Participation form for a project's edition."""

    edition = models.OneToOneField(
        'Edition',
        on_delete=models.CASCADE,
        related_name='edition_form',
        verbose_name='édition')

    form = models.OneToOneField(
        'dynamicforms.Form',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="formulaire d'inscription")

    deadline = models.DateField(
        'date butoir',
        help_text="Les lycéens ne pourront plus s'inscrire après cette date.")

    recipient = models.ForeignKey(
        'profiles.Tutor',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='destinataire',
        validators=[_validate_address_is_set],
        help_text=(
            'Tuteur/tutrice à qui envoyer les pièces justificatives. '
            'Son adresse doit être renseignée dans son profil.'
        ))

    class Meta:  # noqa
        ordering = ('deadline',)
        verbose_name = 'formulaire projet'
        verbose_name_plural = 'formulaires projet'

    def __str__(self):
        return str(self.form)


class ParticipationQuerySet(models.QuerySet):
    """Custom QuerySet for participations."""

    def pending(self):
        """Return pending participations only."""
        return self.filter(state=Participation.STATE_PENDING)

    def validated(self):
        """Return validated participations only."""
        return self.filter(state=Participation.STATE_VALIDATED)

    def accepted(self):
        """Return accepted participations only."""
        return self.filter(state=Participation.STATE_ACCEPTED)

    def rejected(self):
        """Return rejected participations only."""
        return self.filter(state=Participation.STATE_REJECTED)

    def cancelled(self):
        """Return cancelled participations only."""
        return self.filter(state=Participation.STATE_CANCELLED)


class Participation(models.Model):
    """Represents the participation of a user (a student) to a project."""

    objects = ParticipationQuerySet.as_manager()

    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, verbose_name='utilisateur',
        related_name='project_participations')

    edition = models.ForeignKey(
        'Edition', on_delete=models.CASCADE, verbose_name='édition',
        related_name='participations')

    submitted = models.DateTimeField(
        auto_now_add=True, verbose_name='soumis le',
        help_text='Date de soumission de la participation')

    entry = models.OneToOneField(
        'dynamicforms.FormEntry',
        on_delete=models.CASCADE,
        null=True,
        related_name='project_participation',
        verbose_name='entrée',
        help_text="Réponses au formulaire d'inscription",
    )

    STATE_PENDING = 'pending'
    STATE_VALIDATED = 'valid'
    STATE_ACCEPTED = 'accepted'
    STATE_REJECTED = 'rejected'
    STATE_CANCELLED = 'cancelled'

    _STATE_CHOICES = (
        (STATE_PENDING, 'En attente'),
        (STATE_VALIDATED, 'Validé'),
        (STATE_ACCEPTED, 'Accepté'),
        (STATE_REJECTED, 'Refusé'),
        (STATE_CANCELLED, 'Annulé'),
    )

    state = models.CharField(
        'état', max_length=10, choices=_STATE_CHOICES,
        blank=False, default=STATE_PENDING,
        help_text=(
            "État de la participation. "
            "En attente = en cours de validation par les organisateurs. "
            "Validé = toutes les pièces ont été reçues et sont conformes. "
            "Accepté = le lycéen a été sélectionné pour participer. "
            "Refusé = le lycéen n'a pas été sélectionné pour participer. "
            "Annulé = le lycéen a annulé sa participation."
        ))

    class Meta:  # noqa
        ordering = ('-submitted',)

    def __str__(self):
        """Represent by its user."""
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
        """Represent by its user."""
        return str(self.user)
