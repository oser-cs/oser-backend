"""Dynamic forms models.

Concept
-------

A dynamic form is a form stored in the database which can have an undetermined
number of questions of various types (small text, long text, file upload…).

A user can reply to a form by submitting a form entry, made of
multiple answers (one per question).
"""

from django.db import models
from django.utils.text import Truncator, slugify

from .utils import file_upload_to


class Form(models.Model):
    """Represents a form with multiple questions."""

    title = models.CharField('titre', max_length=300)

    slug = models.SlugField(max_length=100, blank=True, default='')

    created = models.DateTimeField('créé le', auto_now_add=True)

    class Meta:  # noqa
        ordering = ('-created',)
        verbose_name = 'formulaire'

    def clean(self):
        """Assign a slug automatically."""
        if not self.pk:
            self.slug = slugify(self.title)

    def __str__(self):
        return str(self.title)

    @property
    def entries_count(self) -> int:
        """Return the number of entries in this form."""
        return self.entries.count()


class Section(models.Model):
    """Represents a group of related questions."""

    title = models.CharField('titre', max_length=100)

    form = models.ForeignKey(
        'Form',
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='formulaire',
        help_text="Formulaire associé à la section.")

    def __str__(self):
        return str(self.title)


class Question(models.Model):
    """Represents a question in a form."""

    TYPE_TEXT_SMALL = 'text-small'
    TYPE_TEXT_LONG = 'text-long'
    TYPE_DATE = 'date'
    TYPE_YES_NO = 'yes-no'
    TYPE_SEX = 'sex'

    TYPES = (
        (TYPE_TEXT_SMALL, 'Texte court'),
        (TYPE_TEXT_LONG, 'Texte long'),
        (TYPE_YES_NO, 'Oui/Non'),
        (TYPE_DATE, 'Date'),
        (TYPE_SEX, 'Sexe'),
    )

    text = models.CharField(
        'intitulé',
        max_length=300,
        help_text='intitulé de la question')

    type = models.CharField(
        'type de question',
        max_length=100,
        choices=TYPES)

    help_text = models.CharField(
        'aide',
        max_length=300,
        blank=True,
        default='',
        help_text='Apporte des précisions sur la question')

    required = models.BooleanField('requis', default=True)

    section = models.ForeignKey(
        'Section',
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='section',
        help_text="Section de formulaire associée à la question.")

    def __str__(self) -> str:
        return f'{self.text}{self.required and "*" or ""}'


class FormEntry(models.Model):
    """Represents answers to a form."""

    form = models.ForeignKey(
        'Form',
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='formulaire',
        help_text="Formulaire associé à l'entrée.")

    submitted = models.DateTimeField(
        'soumis le',
        auto_now_add=True,
        help_text="Date et heure de soumission de l'entrée.")

    class Meta:  # noqa
        ordering = ('-submitted',)
        verbose_name = 'entrée de formulaire'
        verbose_name_plural = 'entrées de formulaire'

    def __str__(self):
        return f'{self.form} ({self.submitted})'


class Answer(models.Model):
    """Represents an answer to a particular question in a form."""

    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='answers')

    entry = models.ForeignKey(
        'FormEntry',
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='entrée',
        help_text="Entrée associée à la réponse.")

    answer = models.TextField('réponse', blank=True, null=True)

    class Meta:  # noqa
        verbose_name = 'réponse'

    def __str__(self):
        answer = Truncator(self.answer).chars(140)
        return f'{self.question} : {answer}'


class File(models.Model):
    """Represents a file downloadable by form respondants."""

    name = models.CharField('nom', max_length=300)

    file = models.FileField('fichier', upload_to=file_upload_to)

    form = models.ForeignKey(
        'Form',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='formulaire')

    class Meta:  # noqa
        verbose_name = 'fichier'
        verbose_name_plural = 'fichiers'

    def __str__(self):
        return str(self.name)
