"""Core models."""

from django.shortcuts import reverse
from django.db import models
from django.utils.text import slugify
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
        if self.pk is None and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('api:document-detail', args=[str(self.slug)])

    def __str__(self):
        return str(self.slug)
