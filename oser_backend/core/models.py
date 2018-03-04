"""Core models."""

from django.db import models

# Create your models here.


class Link(models.Model):
    """Represents a simple link."""

    slug = models.SlugField(unique=True, primary_key=True, help_text=(
        "Un identifiant unique pour ce lien. Privilégiez 'ce-format-de-slug'."
    ))
    url = models.URLField('URL')
    description = models.TextField(help_text=(
        "Précisez ce que contient ce lien et comment il est utilisé."
    ))

    class Meta:  # noqa
        verbose_name = 'lien'

    def __str__(self):
        return str(self.slug)
