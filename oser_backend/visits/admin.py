"""Visits admin panel configuration."""

from django import forms
from django.contrib import admin, messages
from django.template.defaultfilters import pluralize

from .models import Participation, Place, Visit

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

    class Meta:  # noqa
        model = Visit
        fields = '__all__'

    def clean(self):
        """Validate dates and time.

        - Deadline must be before the date
        - End time must be after start time
        """
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        deadline = cleaned_data.get('deadline')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if deadline.date() >= date:
            error = forms.ValidationError(
                "La date limite d'inscription doit être avant la "
                "date de la sortie."
            )
            self.add_error('deadline', error)
        if end_time <= start_time:
            error = forms.ValidationError(
                "L'heure de fin doit être après l'heure de début.")
            self.add_error('start_time', error)
            self.add_error('end_time', error)


class ParticipationInline(admin.StackedInline):
    """Inline for Participation."""

    model = Visit.participants.through
    extra = 0


def accept_selected_participations(modeladmin, request, queryset):
    """Accept selected participations in list view."""
    for obj in queryset:
        obj.accepted = True
        obj.save()
    count = queryset.count()
    s = pluralize(count)
    messages.add_message(request, messages.SUCCESS,
                         f'{count} participation{s} acceptée{s} avec succès.')


accept_selected_participations.short_description = (
    'Accepter les participations sélectionnées')


def reject_selected_participations(modeladmin, request, queryset):
    """Reject selected participations in list view."""
    for obj in queryset:
        obj.accepted = False
        obj.save()
    count = queryset.count()
    s = pluralize(count)
    messages.add_message(request, messages.SUCCESS,
                         f'{count} participation{s} acceptée{s} avec succès.')


reject_selected_participations.short_description = (
    'Rejeter les participations sélectionnées')


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    """Admin panel for visit participations."""

    list_display = ('visit', 'user', 'accepted', 'present')
    list_filter = ('visit',)
    actions = [accept_selected_participations, reject_selected_participations]


@admin.register(Visit.organizers.through)
class VisitOrganizersAdmin(admin.ModelAdmin):
    """Admin panel for visit organizers."""

    list_display = ('visit', 'tutor',)


class OrganizersInline(admin.TabularInline):
    """Inline for visit organizers."""

    model = Visit.organizers.through
    extra = 0


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    """Admin panel for visits."""

    # IDEA create a dashboard using:
    # https://medium.com/@hakibenita/how-to-turn-django-admin-into-a-lightweight-dashboard-a0e0bbf609ad

    form = VisitForm
    inlines = (OrganizersInline, ParticipationInline,)
    list_display = ('__str__', 'place', 'date', 'start_time', 'deadline',
                    '_registrations_open', 'num_participants')
    list_filter = ('date', RegistrationsOpenFilter)
    search_fields = ('title', 'place',)
    exclude = ('participants', 'organizers',)

    def num_participants(self, obj):
        return obj.participants.count()
    num_participants.short_description = 'Participants'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Admin panel for places."""

    list_display = ('name', 'address', 'num_visits', 'last_visit')
    list_display_links = ('name', 'last_visit')

    def num_visits(self, obj):
        return obj.visit_set.count()
    num_visits.short_description = 'Nombre de sorties'

    def last_visit(self, obj):
        return obj.visit_set.passed().order_by('date').first()
    last_visit.short_description = 'Dernière sortie'
