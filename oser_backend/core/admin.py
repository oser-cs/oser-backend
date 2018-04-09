"""Core admin panel configuration."""

from django.contrib import admin
from .models import Document, Address

# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin panel for documents."""

    list_display = ('title', 'slug',)
    readonly_fields = ('slug',)

    # reorganize fields
    fields = ('title', 'slug', 'content',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin panel for addresses."""

    list_display = ('id', '__str__',)
    search_fields = ('line1', 'line2', 'post_code', 'city',)
