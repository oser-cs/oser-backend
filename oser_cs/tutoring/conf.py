"""Tutoring settings."""

from django.conf import settings
from utils import setdefault


setdefault(settings, 'DEFAULT_SESSION_START_TIME', (17, 0))  # (h, m)
setdefault(settings, 'DEFAULT_SESSION_END_TIME', (19, 0))  # (h, m)
