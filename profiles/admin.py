"""Profiles admin panel."""

from django.contrib import admin
from .models import Student, Tutor


class ProfileAdminMixin:
    """Common functionalities for profile admin panels."""

    search_fields = ('user__email', 'user__first_name', 'user__last_name',)


@admin.register(Tutor)
class TutorAdmin(ProfileAdminMixin, admin.ModelAdmin):
    """Tutor admin panel."""

    autocomplete_fields = ('address',)

    class Meta:  # noqa
        model = Tutor


@admin.register(Student)
class StudentAdmin(ProfileAdminMixin, admin.ModelAdmin):
    """Student admin panel."""

    class Meta:  # noqa
        model = Student
