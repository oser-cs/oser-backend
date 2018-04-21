"""Users permissions constants and utilities."""

from django.contrib.auth.models import Group, Permission


class Groups:
    """List of Django user groups that must be defined in the system."""

    # Add more groups below.
    # They will be created at each system check if not already existing.
    # NOTE: Group variable name must start with "G_" to be detected.
    # G_VP_TUTORAT = 'VP Tutorat'
    # G_SECTEUR_SORTIES = 'Secteur sorties'

    # Define permissions of groups here
    perms = {
        # G_SECTEUR_SORTIES: ('change_visit', 'change_place'),
    }

    @classmethod
    def get_names(cls):
        return [getattr(cls, k) for k in dir(Groups) if k.startswith('G_')]


def setup_groups():
    """Setup the necessary users groups for the site to run normally.

    Returns
    -------
    created_groups : dict(str: bool)
        Indicates which groups were created.
    """
    created_groups = {}
    for groupname in Groups.get_names():
        group, created = Group.objects.get_or_create(name=groupname)
        # add permisions to group if defined
        perms = Groups.perms.get(groupname, [])
        for perm in perms:
            try:
                perm_object = Permission.objects.get(codename=perm)
                if perm_object not in group.permissions.all():
                    group.permissions.add(perm_object)
            except Permission.DoesNotExist as e:
                raise ValueError(e)
        else:
            group.save()
        created_groups[groupname] = created
    return created_groups
