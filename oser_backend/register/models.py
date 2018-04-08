"""Register models."""

from django.db import models
from dry_rest_permissions.generics import authenticated_users


# Create your models here.

class Registration(models.Model):
    """Represents a student registration to tutoring activities."""

    first_name = models.CharField(
        max_length=50, verbose_name='prénom',
        help_text='Prénom du lycéen (50 caractères max)')
    last_name = models.CharField(
        max_length=50, verbose_name='nom',
        help_text='Nom du lycéen (50 caracèteres max)')
    email = models.EmailField(
        verbose_name='adresse email',
        help_text=(
            'Adresse email personnelle du lycéen '
            '(doit être une adresse mail valide)'
        ))
    phone = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='téléphone',
        help_text=(
            "Numéro de téléphone personnel du lycéen (30 caracètres max). "
            "Note : le format n'est pas vérifié."
        ))
    date_of_birth = models.DateField(
        verbose_name='date de naissance',
        help_text="Date de naissance du lycéen")
    submitted = models.DateTimeField(
        auto_now_add=True, verbose_name='envoyé le',
        help_text="Date d'envoi du dossier d'inscription")

    class Meta:  # noqa
        ordering = ('-submitted',)
        verbose_name = "dossier d'inscription"
        verbose_name_plural = "dossiers d'inscription"

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_create_permission(request):
        return True

    def __str__(self):
        return '{o.first_name} {o.last_name} ({o.submitted})'.format(o=self)
