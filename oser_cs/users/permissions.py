"""Users permissions constants and utilities."""

from django.contrib.auth.models import Group


class Groups:
    """Define Users groups here."""

    VP_TUTORAT = 'VP Tutorat'

    @classmethod
    def get_names(cls):
        return [getattr(cls, k) for k in dir(Groups)
                if not callable(getattr(cls, k)) and
                not k.startswith('__')]


def setup_groups():
    """Setup the necessary users groups for the site to run normally.

    Returns
    -------
    created_groups : dict(str: bool)
        Indicates which groups were created.
    """
    created_groups = {}
    for groupname in Groups.get_names():
        _, created = Group.objects.get_or_create(name=groupname)
        created_groups[groupname] = created
    return created_groups
