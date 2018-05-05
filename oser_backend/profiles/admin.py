"""Profiles admin panel."""

from django.contrib import admin
from .models import Student, Tutor
from tutoring.models import TutoringGroup


class ProfileAdminMixin:
    """Common functionalities for profile admin panels."""

    search_fields = ('user__email', 'user__first_name', 'user__last_name',)


class TutorTutoringGroupsInline(admin.TabularInline):
    """Inline for tutor tutoring groups."""

    model = TutoringGroup.tutors.through
    extra = 0
    max_num = 0
    readonly_fields = ('tutoring_group', 'is_leader')
    can_delete = False


@admin.register(Tutor)
class TutorAdmin(ProfileAdminMixin, admin.ModelAdmin):
    """Tutor admin panel."""

    inlines = (TutorTutoringGroupsInline,)

    class Meta:  # noqa
        model = Tutor


@admin.register(Student)
class StudentAdmin(ProfileAdminMixin, admin.ModelAdmin):
    """Student admin panel."""

    class Meta:  # noqa
        model = Student
