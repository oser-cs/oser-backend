"""Register models."""

from django.db import models
from dry_rest_permissions.generics import authenticated_users


# Create your models here.

class Registration(models.Model):
    """Represents a student registration to tutoring activities."""

    # NOTE: this model is bound to evolve as the registration data
    # expands.

    first_name = models.CharField(max_length=50,
                                  verbose_name='prénom')
    last_name = models.CharField(max_length=50, verbose_name='nom')
    email = models.EmailField(verbose_name='adresse email')
    phone = models.CharField(max_length=30,
                             blank=True, null=True,
                             verbose_name='téléphone')
    date_of_birth = models.DateField(blank=False, null=True,
                                     verbose_name='date de naissance')
    submitted = models.DateTimeField(auto_now_add=True,
                                     verbose_name='envoyé le')

    class Meta:  # noqa
        ordering = ('-submitted',)
        verbose_name = 'inscription administrative'
        verbose_name_plural = 'inscriptions administratives'

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @authenticated_users
    def has_create_permission(request):
        return True

    def __str__(self):
        return '{o.first_name} {o.last_name} ({o.submitted})'.format(o=self)
