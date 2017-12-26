"""Users permissions constants and utilities."""

from django.contrib.auth.models import Group


class Groups:
    """Define Users groups here."""
    VP_TUTORAT = 'VP Tutorat'

    @classmethod
    def get_names(cls):
        return (getattr(cls, k) for k in dir(Groups)
                if not callable(k) and not k.startswith('__'))


def setup_groups():
    for groupname in Groups.get_names():
        Group.objects.get_or_create(name=groupname)
