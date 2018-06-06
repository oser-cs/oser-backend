"""Register admin panels."""

from django.contrib import admin
from django.utils.html import format_html
from core.admin import AutocompleteAddressMixin
from .models import Registration, EmergencyContact

# Register your models here.


@admin.register(Registration)
class RegistrationAdmin(AutocompleteAddressMixin, admin.ModelAdmin):
    """Admin panel for registrations."""

    list_display = ('last_name', 'first_name', 'school', 'grade', 'submitted')
    readonly_fields = ('submitted',)
    list_filter = ('submitted', 'school', 'grade',)
    autocomplete_fields = ('emergency_contact', 'school',)


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """Admin panel for emergency contacts."""

    list_display = ('last_name', 'first_name',
                    'email', 'home_phone', 'mobile_phone', 'related_student',)
    search_fields = ('last_name', 'first_name',)

    def related_student(self, obj):
        """Link to the contact's registration object."""
        url = '/admin/register/registration/{}'.format(obj.registration.pk)
        return format_html(
            '<a href="{}">{}</a>',
            url, str(obj.registration)
        )
    related_student.short_description = "Inscription administrative associée"
