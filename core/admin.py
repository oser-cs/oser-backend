"""Core admin panel configuration."""

from django.contrib import admin
from .models import Document, Address
from django.http import HttpResponse
import csv
# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin panel for documents."""

    list_display = ('title', 'slug',)
    readonly_fields = ('slug',)

    # reorganize fields
    fields = ('title', 'slug', 'content',)

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])
        return response
    export_as_csv.short_description = "Exporter au format CSV"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin panel for addresses."""

    list_display = ('id', '__str__',)
    search_fields = ('line1', 'line2', 'post_code', 'city',)


class AutocompleteAddressMixin:
    """Enable autocompletion on the address field of a model.

    Class Attributes
    ----------------
    address_field_name : str, optional
        The name of the address field on the model. Default is 'address'.
    """

    address_field_name = 'address'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = getattr(self, 'autocomplete_fields', ())
        if self.address_field_name not in initial:
            self.autocomplete_fields = initial + (self.address_field_name,)
