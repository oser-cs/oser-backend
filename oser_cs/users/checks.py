"""Users app system checks."""

from django.core.checks import Info, register, Tags
from users.permissions import setup_groups


@register(Tags.models)
def groups_check(app_configs, **kwargs):
    """Check for users groups and add those missing as necessary."""
    errors = []
    groups_created = setup_groups()
    for groupname, created in groups_created.items():
        if created:
            errors.append(
                Info(
                    'Created group: {}'.format(groupname),
                    hint=(
                        'This happened because the system needs this group '
                        'to run correctly'
                    ),
                    id='users.I001')
            )
    return errors
