"""Tutoring admin panel configuration."""

from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html
from core.admin import AutocompleteAddressMixin
from users.models import Student
from .models import TutoringGroup, School, TutoringSession

# Register your models here.


class TutoringGroupMembershipInline(admin.TabularInline):
    """Inline for tutoring group membership."""

    model = TutoringGroup.tutors.through
    extra = 0


class TutoringGroupStudentsInline(admin.TabularInline):
    """Inline to show students in a tutoring group."""

    model = Student
    extra = 0
    max_num = 0
    readonly_fields = ('user', 'school',)
    can_delete = False


@admin.register(TutoringGroup)
class TutoringGroupAdmin(admin.ModelAdmin):
    """Tutoring group admin panel."""

    inlines = [
        TutoringGroupStudentsInline,
        TutoringGroupMembershipInline,
    ]
    search_fields = ('name',)

    class Meta:  # noqa
        model = TutoringGroup


@admin.register(School)
class SchoolAdmin(AutocompleteAddressMixin, admin.ModelAdmin):
    """School admin panel."""

    list_display = ('__str__', 'uai_code',
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


@admin.register(TutoringSession)
class TutoringSessionAdmin(admin.ModelAdmin):
    """Tutoring session admin panel."""

    list_display = ('__str__', 'link_tutoring_group', 'link_school', 'date',)
    autocomplete_fields = ('tutoring_group',)

    def link_tutoring_group(self, obj):
        link = reverse('admin:tutoring_tutoringgroup_change',
                       args=[obj.tutoring_group.pk])
        s = str(obj.tutoring_group)
        return format_html("<a href='{link}'>{s}</a>", link=link, s=s)
    link_tutoring_group.admin_order_field = 'groupe de tutorat'
    link_tutoring_group.short_description = 'groupe de tutorat'

    def link_school(self, obj):
        if not obj.school:
            return None
        link = reverse('admin:tutoring_school_change',
                       args=[obj.school.pk])
        s = str(obj.school)
        return format_html("<a href='{link}'>{s}</a>", link=link, s=s)
    link_school.admin_order_field = 'lycée'
    link_school.short_description = 'lycée'

    class Meta:  # noqa
        model = TutoringSession
