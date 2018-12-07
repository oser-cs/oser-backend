"""Users admin panel configuration."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from visits.admin import ParticipationInline

from .models import User
from django.http import HttpResponse
import csv


class UserParticipationInline(ParticipationInline):
    """Inline for Participation on the User admin panel.

    All fields are read-only.
    """

    readonly_fields = ('user', 'visit', 'accepted', 'present',)
    verbose_name = 'Participation aux sorties'
    verbose_name_plural = 'Participation aux sorties'

    def has_add_permission(self, request):
        return False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Customized user admin panel."""

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [field for field in UserAdmin.list_display
                    if field != 'username']
    search_fields = search_fields = (
        'email', 'first_name', 'last_name',)
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'phone_number',
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    inlines = (UserParticipationInline, )

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
