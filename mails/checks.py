"""Mails app system checks."""

from django.conf import settings
from django.core.checks import Warning, register


@register()
def check_sendgrid_api_key_is_set(app_configs, **kwargs):
    errors = []

    if getattr(settings, 'SENDGRID_API_KEY', None) is None:
        errors.append(
            Warning(
                'SENDGRID_API_KEY is not set, sending emails will fail',
                obj=settings,
                id='mails.W001',
            )
        )

    return errors
