"""Register admin panels."""

from django.contrib import admin
from .models import Registration, EmergencyContact

# Register your models here.


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """Admin panel for registrations."""

    list_display = ('id', 'first_name', 'last_name', 'submitted')
    readonly_fields = ('submitted',)
    list_filter = ('submitted',)
    autocomplete_fields = ('address', 'emergency_contact')


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """Admin panel for emergency contacts."""

    list_display = ('last_name', 'first_name', 'contact', 'registration',)

    # necessary to use emergency contact in Registration's admin autocomplete
    search_fields = ('last_name', 'first_name',)
