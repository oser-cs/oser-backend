"""Users admin panel configuration."""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .models import User, Tutor, Student, SchoolStaffMember
from tutoring.admin import TutoringGroupMembershipInline
from visits.admin import VisitParticipantInline


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


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    """Tutor admin panel."""

    inlines = (TutoringGroupMembershipInline,)

    class Meta:  # noqa
        model = Tutor


class StudentVisitParticipantInline(VisitParticipantInline):
    """Inline for VisitParticipant on the Student admin panel.

    All fields are read-only.
    """

    readonly_fields = ('student', 'visit', 'present')
    verbose_name = 'Participation aux sorties'
    verbose_name_plural = 'Participation aux sorties'

    def has_add_permission(self, request):
        return False


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Student admin panel."""

    inlines = (StudentVisitParticipantInline, )

    class Meta:  # noqa
        model = Student


@admin.register(SchoolStaffMember)
class SchoolStaffMemberAdmin(admin.ModelAdmin):
    """School staff member admin panel."""

    class Meta:  # noqa
        model = SchoolStaffMember
