"""Mails app settings."""
from django.conf import settings
import warnings

NOTIFICATIONS_ADDRESS = getattr(settings, 'MAILS_NOTIFICATIONS_ADDRESS')
ENABLED = getattr(settings, 'MAILS_ENABLED')
RAISE_EXCEPTIONS = getattr(settings, 'MAILS_RAISE_EXCEPTIONS')

if getattr(settings, 'SENDGRID_API_KEY', None) is None:
    warnings.warn('SENDGRID_API_KEY is not set, sending emails will fail')
