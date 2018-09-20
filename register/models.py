"""Register models."""

from django.db import models


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
            'Adresse email personnelle du lycéen. '
            'Note : doit être une adresse mail valide.'
        ))
    phone_number = models.CharField(
        max_length=20, verbose_name='téléphone',
        help_text='Numéro de téléphone du lycéen (20 caractères max)',
        blank=False, default='',
    )
    submitted = models.DateTimeField(
        auto_now_add=True, verbose_name='envoyé le',
        help_text="Date d'envoi du dossier d'inscription")
    validated = models.BooleanField(
        default=False, verbose_name='validé',
        help_text=(
            "Cocher pour valider le dossier d'inscription. "
            "Le lycéen pourra alors avoir accès à toutes les fonctionnalités "
            "associées à son profil."
        )
    )

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

    @property
    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        return '{o.full_name} ({o.submitted})'.format(o=self)
