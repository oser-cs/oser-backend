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
    phone = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='téléphone',
        help_text=(
            "Numéro de téléphone personnel du lycéen (30 caracètres max). "
            "Note : le format n'est pas vérifié."
        ))
    date_of_birth = models.DateField(
        verbose_name='date de naissance',
        help_text="Date de naissance du lycéen")
    address = models.ForeignKey(
        'core.Address', on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='adresse',
        help_text="Adresse du lycéen")
    emergency_contact = models.OneToOneField(
        'EmergencyContact',
        on_delete=models.CASCADE, blank=True, null=True,
        verbose_name="contact d'urgence",
        help_text="Contact en cas d'urgence.")
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


class EmergencyContact(models.Model):
    """Represents an emergency contact for a student."""

    first_name = models.CharField(
        'prénom', max_length=50,
        help_text='Prénom du contact (50 caractères max).'
    )
    last_name = models.CharField(
        'nom', max_length=50,
        help_text='Nom du contact (50 caractères max).'
    )
    email = models.EmailField(
        verbose_name='adresse email',
        blank=True, null=True,
    )
    home_phone = models.CharField(
        'téléphone fixe', max_length=50,
        blank=True, null=True,
    )
    mobile_phone = models.CharField(
        'téléphone portable', max_length=50,
        blank=True, null=True,
    )

    def __str__(self):
        """Represent the emergency contact by its full name."""
        return '{o.first_name} {o.last_name}'.format(o=self)

    class Meta:  # noqa
        verbose_name = "contact d'urgence"
        verbose_name_plural = "contacts d'urgence"
        ordering = ('last_name', 'first_name',)
