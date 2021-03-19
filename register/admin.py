"""Register admin panels."""

from django.contrib import admin
from .models import Registration
from profiles.models import Student


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
            return queryset.filter(email__in=emails)


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
            return queryset.filter(email__in=emails)


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
            return queryset.filter(email__in=emails)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """Admin panel for registrations."""

    list_display = ('last_name', 'first_name', 'submitted')
    readonly_fields = ('submitted',)
    list_filter = (SchoolFilter,
                   'submitted', 'validated')
