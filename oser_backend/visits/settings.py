"""Visits app settings."""

from django.conf import settings

# Email address of OSER's visits team
TEAM_EMAIL = getattr(settings, 'VISITS_TEAM_EMAIL')
