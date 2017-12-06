"""Users admin panel configuration."""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .models import (
    User, Tutor, TutoringGroup,
)

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Customized user admin panel."""

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [field for field in UserAdmin.list_display
                    if field != 'username']
    search_fields = [field for field in UserAdmin.search_fields
                     if field != 'username']
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone_number',
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


class TutoringGroupMembershipInline(admin.TabularInline):
    model = TutoringGroup.tutors.through
    extra = 0


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """Tutor admin panel."""

    inlines = [
        TutoringGroupMembershipInline
    ]

    class Meta:  # noqa
        model = Tutor


@admin.register(TutoringGroup)
class TutoringGroupAdmin(admin.ModelAdmin):
    """Tutoring group admin panel."""

    inlines = [
        TutoringGroupMembershipInline
    ]

    class Meta:  # noqa
        model = TutoringGroup
