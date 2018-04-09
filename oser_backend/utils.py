"""Various utilities."""

from string import printable
from django.contrib.auth.models import Group


def modify_fields(**kwargs):
    """Modify the fields of an inherited model.

    Caution: will affect the inherited model's fields too. It is preferable to
    restrict the usage to cases when the inherited model is abstract.

    Example
    -------
    class Foo(models.Model):
        health = models.IntegerField()

    @modify_fields(health={'blank': True})
    class Bar(models.Model):
        pass
    """
    def wrap(cls):
        for field, prop_dict in kwargs.items():
            for prop, val in prop_dict.items():
                setattr(cls._meta.get_field(field), prop, val)
        return cls
    return wrap


def setdefault(d, attr, default):
    """Set an attribute of an object if not present.

    Equivalent of dict's setdefault() but for objects.
    Typically used for configuring app settings.
    """
    if not hasattr(d, attr):
        setattr(d, attr, default)
    return d


def is_in_group(user, group_name):
    """Return True if user is in group."""
    return (Group.objects.get(name=group_name)
            .user_set
            .filter(id=user.id)
            .exists())


def group_exists(group_name):
    """Return True if group exists."""
    return Group.objects.filter(name=group_name).exists()


def printable_only(s, with_spaces=False):
    """Remove non-printable characters from a string."""
    filtered = ''.join(c for c in filter(lambda x: x in printable, s))
    if not with_spaces:
        return filtered.replace(' ', '')
    return filtered
