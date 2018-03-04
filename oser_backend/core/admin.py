"""Showcase site admin panel configuration."""

from django.contrib import admin
from .models import Link


# Register your models here.

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """Link admin panel."""

    list_display = ('__str__', 'description')
