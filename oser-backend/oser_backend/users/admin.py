"""Users admin panel configuration."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from guardian.admin import GuardedModelAdminMixin

from tutoring.admin import TutoringGroupMembershipInline
from visits.admin import VisitParticipantInline

from .models import SchoolStaffMember, Student, Tutor, User


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

    inlines = (UserVisitParticipantInline, )


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """Tutor admin panel."""

    inlines = (TutoringGroupMembershipInline,)

    class Meta:  # noqa
        model = Tutor


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Student admin panel."""

    class Meta:  # noqa
        model = Student


@admin.register(SchoolStaffMember)
class SchoolStaffMemberAdmin(admin.ModelAdmin):
    """School staff member admin panel."""

    class Meta:  # noqa
        model = SchoolStaffMember
