"""Mails app settings."""
from django.conf import settings

NOTIFICATIONS_ADDRESS = getattr(
    settings, 'MAILS_NOTIFICATIONS_ADDRESS', 'notifications@oser-cs.fr')
ENABLED = getattr(settings, 'MAILS_ENABLED')
