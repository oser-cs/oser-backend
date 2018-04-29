"""Users admin panel configuration."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from guardian.admin import GuardedModelAdminMixin

from core.admin import AutocompleteAddressMixin
from visits.admin import VisitParticipantInline

from .models import Student, Tutor, User


# Register your models here.

class UserVisitParticipantInline(VisitParticipantInline):
    """Inline for VisitParticipant on the User admin panel.

    All fields are read-only.
    """

    readonly_fields = ('user', 'visit', 'accepted', 'present',)
    verbose_name = 'Participation aux sorties'
    verbose_name_plural = 'Participation aux sorties'

    def has_add_permission(self, request):
        return False


@admin.register(User)
class CustomUserAdmin(GuardedModelAdminMixin, UserAdmin):
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

    inlines = (UserVisitParticipantInline, )


class ProfileAdminMixin:
    """Common functionalities for profile admin panels."""

    search_fields = ('user__email', 'user__first_name', 'user__last_name',)


class TutorTutoringGroupsInline(admin.TabularInline):
    """Inline for tutor tutoring groups."""

    model = Tutor.tutoring_groups.through
    extra = 0
    max_num = 0
    readonly_fields = ('tutoring_group', 'is_leader')
    can_delete = False


@admin.register(Tutor)
class TutorAdmin(ProfileAdminMixin, admin.ModelAdmin):
    """Tutor admin panel."""

    inlines = (TutorTutoringGroupsInline,)

    class Meta:  # noqa
        model = Tutor


@admin.register(Student)
class StudentAdmin(AutocompleteAddressMixin, ProfileAdminMixin,
                   admin.ModelAdmin):
    """Student admin panel."""

    class Meta:  # noqa
        model = Student
