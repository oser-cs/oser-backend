"""Core models."""

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from django_countries.fields import CountryField
from markdownx.models import MarkdownxField


class Document(models.Model):
    """Represents a simple document, with a title and a text content.

    Markdown support integrated.
    """

    title = models.CharField('titre', max_length=300,
                             help_text="Titre du document")
    slug = models.SlugField(
        max_length=100, unique=True,
        help_text=(
            "Un court identifiant généré après la création du document."
        ))
    content = MarkdownxField(
        'contenu',
        help_text="Contenu du document (Markdown est supporté).")

    class Meta:  # noqa
        ordering = ('title',)

    def save(self, *args, **kwargs):
        """Save slug as slugified title by default."""
        if self.pk is None and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('api:document-detail', args=[str(self.slug)])

    def __str__(self):
        return str(self.slug)


class Address(models.Model):
    """Represents a physical address."""

    line1 = models.CharField(
        verbose_name='ligne 1', max_length=300,
        help_text="Numéro, voie, rue…",
    )
    line2 = models.CharField(
        verbose_name='ligne 2', max_length=300, default='', blank=True,
        help_text="Résidence, appartement, lieu-dit…",
    )
    post_code = models.CharField(
        verbose_name='code postal', max_length=20,
        help_text="Code postal. Note : le format n'est pas vérifié.",
    )
    city = models.CharField(
        verbose_name='ville', max_length=100,
        help_text='Ville',
    )
    country = CountryField(
        verbose_name='pays',
        default='FR',
        help_text="Pays (FR par défaut).",
    )

    class Meta:  # noqa
        verbose_name = 'adresse'

    def __str__(self):
        return ', '.join(filter(None, [
            self.line1,
            self.line2,
            self.post_code + ' ' + self.city,
            self.country.name,
        ]))
