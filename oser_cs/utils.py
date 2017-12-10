"""Various utilities."""


def modify_fields(**kwargs):
    """Modify the fields of a superclass.

    Caution: will affect the superclass' fields too. It is preferable to
    restrict the usage to cases when the superclass is abstract.

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
