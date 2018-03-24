"""Core admin panel configuration."""

from django.contrib import admin
from .models import Document

# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin panel for documents."""

    list_display = ('title', 'slug',)
    readonly_fields = ('slug',)

    # reorganize fields
    fields = ('title', 'slug', 'content',)
