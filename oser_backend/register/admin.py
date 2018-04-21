"""Register admin panels."""

from django.contrib import admin
from django.utils.html import format_html
from core.admin import AutocompleteAddressMixin
from .models import Registration, EmergencyContact

# Register your models here.


@admin.register(Registration)
class RegistrationAdmin(AutocompleteAddressMixin, admin.ModelAdmin):
    """Admin panel for registrations."""

    list_display = ('last_name', 'first_name', 'submitted')
    readonly_fields = ('submitted',)
    list_filter = ('submitted',)
    autocomplete_fields = ('emergency_contact',)


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """Admin panel for emergency contacts."""

    list_display = ('last_name', 'first_name', 'contact', 'registration_link',)
    list_display_links = ('registration_link',)

    # necessary to use emergency contact in Registration's admin autocomplete
    search_fields = ('last_name', 'first_name',)

    def registration_link(self, obj):
        """Link to the contact's registration object."""
        url = '/admin/register/registration/{}'.format(obj.registration.pk)
        return format_html(
            '<a href="{}">{}</a>',
            url, str(obj.registration)
        )
