"""Profiles admin panel."""

from django.contrib import admin
from .models import Student, Tutor
from .MultiSelectFieldListFilter import MultiSelectFieldListFilter
import codecs

import csv
from django.http import HttpResponse
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        response.write(codecs.BOM_UTF8) #force response to be UTF-8
        writer = csv.writer(response, delimiter=';')

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exporter sélection (en .csv)"


class ProfileAdminMixin:
    """Common functionalities for profile admin panels."""

    search_fields = ('user__email', 'user__first_name', 'user__last_name',)
    actions = ["export_as_csv"]

@admin.register(Tutor)
class TutorAdmin(ProfileAdminMixin, admin.ModelAdmin,ExportCsvMixin):
    """Tutor admin panel."""

    autocomplete_fields = ('address',)

    class Meta:  # noqa
        model = Tutor
    actions = ["export_as_csv"]


@admin.register(Student)
class StudentAdmin(ProfileAdminMixin, admin.ModelAdmin,ExportCsvMixin):
    """Student admin panel."""
    list_filter = (('school',MultiSelectFieldListFilter), 'year', 'registration__validated')
    class Meta:  # noqa
        model = Student
    ordering = ['-updated_date']
    actions = ["export_as_csv"]
