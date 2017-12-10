"""Tutoring admin panel configuration."""


from django.contrib import admin
from .models import TutoringGroup, School

# Register your models here.


class TutoringGroupMembershipInline(admin.TabularInline):
    """Inline for tutoring group membership."""

    model = TutoringGroup.tutors.through
    extra = 0


@admin.register(TutoringGroup)
class TutoringGroupAdmin(admin.ModelAdmin):
    """Tutoring group admin panel."""

    inlines = [
        TutoringGroupMembershipInline
    ]

    class Meta:  # noqa
        model = TutoringGroup


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    """School admin panel."""

    list_display = ('name', 'uai_code',
                    'get_student_count', 'get_groups_count')

    def get_student_count(self, obj):
        return obj.students.count()
    get_student_count.short_description = 'Nombre de lycéens'

    def get_groups_count(self, obj):
        return obj.tutoring_groups.count()
    get_groups_count.short_description = 'Nombre de groupes de tutorat'

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ['uai_code']
        return []

    class Meta:  # noqa
        model = School
