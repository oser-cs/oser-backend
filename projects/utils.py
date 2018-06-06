"""Projects utilities."""

from django.utils import timezone


def this_year() -> int:
    """Return the current year."""
    return timezone.now().year
