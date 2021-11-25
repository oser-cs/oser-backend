"""Visits admin panel configuration."""

from django import forms
from django.contrib import admin, messages
from django.template.defaultfilters import pluralize
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import csv
from .models import Participation, Place, Visit
from profiles.models import Student
from users.models import User
import codecs

# Register your models here.


class SchoolFilter(admin.SimpleListFilter):
    title = 'établissement'
    parameter_name = 'profiles__school'

    def lookups(self, request, model_admin):
        list_of_school = []
        query = Student.objects.values_list(
            "school", flat=True).distinct()
        for school in query:
            list_of_school.append((school, school))
        return list_of_school

    def queryset(self, request, queryset):
        if self.value():
            emails = Student.objects.filter(
                school=self.value()).values_list("user__email", flat=True)
            return queryset.filter(user__email__in=emails)


class RegistrationsOpenFilter(admin.SimpleListFilter):
    """Custom filter to filter visits by their registration openness.

    In Django docs:
    https://docs.djangoproject.com/fr/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    """

    title = 'état des inscriptions'
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

        Keep in mind that values may be `None` if not provided in the form.
        """
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        deadline = cleaned_data.get('deadline')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if deadline is not None:
            if deadline.date() >= date:
                error = forms.ValidationError(
                    "La date limite d'inscription doit être avant la "
                    "date de la sortie."
                )
                self.add_error('deadline', error)
        if end_time is not None and start_time is not None:
            if end_time <= start_time:
                error = forms.ValidationError(
                    "L'heure de fin doit être après l'heure de début.")
                self.add_error('start_time', error)
                self.add_error('end_time', error)


class ParticipationInline(admin.TabularInline):
    """Inline for Participation."""
    # template = "visits/visit_tabular.md"
    actions = ["export_as_csv"]
    model = Visit.participants.through
    extra = 0
    fields = ('name', 'school', 'user', 'submitted', 'present')
    readonly_fields = ('name', 'school', 'user', 'submitted')

    def school(self, participation: Participation):
        """Return a link to the participation's user's school."""
        school = Student.objects.get(user=participation.user).school
        return school
    school.short_description = "Établissement"

    def name(self, participation: Participation):
        """Returns the participation's user's name"""
        return participation.user.first_name + " " + participation.user.last_name
    name.short_description = "Nom"

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}


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

    list_display = ('submitted', 'visit', 'user_link', 'accepted', 'present')
    list_filter = (SchoolFilter, 'submitted', 'accepted', 'present')
    actions = [accept_selected_participations, reject_selected_participations]

    def user_link(self, participation: Participation):
        """Return a link to the participation's user."""
        url = reverse("admin:users_user_change", args=[participation.user.id])
        link = f'<a href="{url}">{participation.user}</a>'
        return mark_safe(link)

    user_link.short_description = 'Utilisateur'

    actions = ["export_as_csv"]

    def school(self, participation: Participation):
        """Return a link to the participation's user's school."""
        school = Student.objects.get(user=participation.user).school
        return school
    school.short_description = "Établissement"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        response.write(codecs.BOM_UTF8)  # force response to be UTF-8
        writer = csv.writer(response, delimiter=';')

        writer.writerow(['first_name', 'last_name', 'school', 'grade',
                         'phone_number', 'scholarship'] + field_names)

        list_email = queryset.values_list("user__email", flat=True)
        nb_user = 0
        for obj in queryset:

            name = User.objects.filter(
                email=str(list_email[nb_user])).values('first_name', 'last_name', 'phone_number')
            school = Student.objects.filter(
                user__email=str(list_email[nb_user])).values('school', 'grade', 'scholarship')

            row = writer.writerow([name[0]['first_name'], name[0]['last_name'], school[0]['school'], school[0]['grade'], name[0]['phone_number'], school[0]['scholarship']] + [getattr(obj, field)
                                                                                                                                                                               for field in field_names])

            nb_user += 1
        return response

    export_as_csv.short_description = "Exporter sélection (en .csv)"


@ admin.register(Visit.organizers.through)
class VisitOrganizersAdmin(admin.ModelAdmin):
    """Admin panel for visit organizers."""

    list_display = ('visit', 'tutor',)


class OrganizersInline(admin.TabularInline):
    """Inline for visit organizers."""

    model = Visit.organizers.through
    extra = 0


@ admin.register(Visit)
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


@ admin.register(Place)
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
