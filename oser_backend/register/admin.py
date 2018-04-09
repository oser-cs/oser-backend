"""Register admin panels."""

from django.contrib import admin
from .models import Registration

# Register your models here.


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """Admin panel for registrations."""

    list_display = ('id', 'first_name', 'last_name', 'submitted')
    readonly_fields = ('submitted',)
    list_filter = ('submitted',)
    autocomplete_fields = ('address',)
