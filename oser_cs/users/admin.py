"""Users admin panel configuration."""

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User

# Register your models here.


@admin.register(User)
class UserAdminWithExtraFields(UserAdmin):
    """User admin panel, adding extra fields to the bottom of the page."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        abstract_fields = [field.name for field in AbstractUser._meta.fields]
        user_fields = [field.name for field in self.model._meta.fields]

        self.fieldsets += (
            (_('Autres champs'), {
                'fields': [
                    field for field in user_fields if (
                        field not in abstract_fields and
                        field != self.model._meta.pk.name
                    )
                ],
            }),
        )
