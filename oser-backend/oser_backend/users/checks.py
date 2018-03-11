"""Users app system checks."""

from django.db.utils import OperationalError, ProgrammingError
from django.core.checks import Warning, Info, Error, register, Tags
from users.permissions import setup_groups


@register(Tags.models)
def check_groups(app_configs, **kwargs):
    """Check for users groups and add those missing as necessary."""
    errors = []
    try:
        groups_created = setup_groups()
        for groupname, created in groups_created.items():
            if created:
                errors.append(
                    Info(
                        'Created group: {}'.format(groupname),
                        hint=(
                            'This happened because the system needs this '
                            'group to run correctly'
                        ),
                        id='users.I001')
                )
    except ValueError as e:
        errors.append(Error(
            'Unexpected error: ' + str(e),
            id='users.E001',
        ))
    except (OperationalError, ProgrammingError):
        errors.append(Warning(
            'Could not create groups',
            hint=(
                'This is normal if these are the very first system checks, '
                'because auth_group table is not yet created.'
            ),
            id='users.W001',
        ))

    return errors
