"""Tutoring admin panel configuration."""


from django.contrib import admin
from .models import TutoringGroup

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
