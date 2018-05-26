"""Mails app settings."""
from django.conf import settings
import warnings

NOTIFICATIONS_ADDRESS = getattr(settings, 'MAILS_NOTIFICATIONS_ADDRESS')
ENABLED = getattr(settings, 'MAILS_ENABLED')
SENDGRID_API_KEY = getattr(settings, 'SENDGRID_API_KEY', None)
if SENDGRID_API_KEY is None:
    warnings.warn('SENDGRID_API_KEY not set, emails will not be delivered')
