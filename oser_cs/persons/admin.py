"""Persons admin panel configuration."""

from django.contrib import admin
from persons.models import Tutor
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
