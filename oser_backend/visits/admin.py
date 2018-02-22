"""Visits admin panel configuration."""

from django import forms
from django.contrib import admin
from .models import Visit

# Register your models here.


class RegistrationsOpenFilter(admin.SimpleListFilter):
    """Custom filter to filter visits by their registration openness.

    In Django docs:
    https://docs.djangoproject.com/fr/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    """

    title = "état des inscriptions"
    parameter_name = 'registrations_open'

    def lookups(self, request, model_admin):
        yield (False, 'Fermées')
        yield (True, 'Ouvertes')

    def queryset(self, request, queryset):
        registrations_open = self.value()
        if registrations_open is None:
            return queryset
        return queryset.registrations_open(state=registrations_open)

    def value(self):
        """Convert the querystring value to a nullable boolean."""
        value = super().value()
        return {None: None, 'True': True, 'False': False}[value]


class VisitForm(forms.ModelForm):
    """Custom admin form for Visit."""

    def clean(self):
        """Validate that the deadline is before the date date."""
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        deadline = cleaned_data.get('deadline')
        if deadline >= date:
            error = forms.ValidationError(
                "La date limite d'inscription doit être avant la "
                "date de la sortie."
            )
            self.add_error('deadline', error)


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    """Admin panel for visits."""

    form = VisitForm
    list_display = ('__str__', 'place', 'date', 'deadline',
                    '_registrations_open', 'fact_sheet')
    list_filter = ('date', RegistrationsOpenFilter)
    search_fields = ('title', 'place',)
