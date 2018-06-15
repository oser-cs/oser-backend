"""Mails app settings."""
from django.conf import settings

NOTIFICATIONS_ADDRESS = getattr(settings, 'MAILS_NOTIFICATIONS_ADDRESS')
ENABLED = getattr(settings, 'MAILS_ENABLED')
RAISE_EXCEPTIONS = getattr(settings, 'MAILS_RAISE_EXCEPTIONS')
