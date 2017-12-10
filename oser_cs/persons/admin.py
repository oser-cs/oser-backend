"""Persons admin panel configuration."""

from django.contrib import admin
from persons.models import Tutor, Student, SchoolStaffMember
from tutoring.admin import TutoringGroupMembershipInline

# Register your models here.


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """Tutor admin panel."""

    inlines = [
        TutoringGroupMembershipInline
    ]

    class Meta:  # noqa
        model = Tutor


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Student admin panel."""

    class Meta:  # noqa
        model = Student


@admin.register(SchoolStaffMember)
class SchoolStaffMemberAdmin(admin.ModelAdmin):
    """School staff member admin panel."""

    class Meta:  # noqa
        model = SchoolStaffMember
