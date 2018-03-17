"""Utils for populatedb."""

import os
import re
import string
from itertools import cycle
from contextlib import contextmanager

from django.core.files import File
from django.db.models.base import ModelBase
from factory.base import FactoryMetaClass

HERE = os.path.dirname(os.path.abspath(__file__))


def format_keys(s):
    """Return tuple of format keys in s.

    format_keys('Hi {person}. Eat {food}? {}') => ('person', 'good', '')
    """
    formatter = string.Formatter()
    return tuple(tup[1] for tup in formatter.parse(s) if tup[1] is not None)


assert format_keys('Hi {person}. Eat {food}? {}') == ('person', 'food', '')


class DataLoader:
    """Simple utility class to load data files."""

    def __init__(self, path=None):
        if path is None:
            path = os.path.join(HERE, 'data')
        self.path = path

    @contextmanager
    def load(self, filename):
        """Load a single file and return it as a Django File object."""
        path = os.path.join(self.path, filename)
        f = open(path, 'rb')
        try:
            wrapped_file = File(f)
            # Default name of the file is the full path to file.
            # Use only the filename.
            wrapped_file.name = filename
            yield wrapped_file
        finally:
            f.close()


class SeqDataLoader(DataLoader):
    """Iterable that yields filenames to a given amount of resources.

    Resources are cycled through if the required amount exceeds
    the amount of resources available.

    Usage
    -----
    for filename in DataLoader('resource-{i}.txt', 6):
        with open(filename) as text:
            print(text)
    """

    def __init__(self, resource_format, amount, **kwargs):
        super().__init__(**kwargs)
        self.pattern = self._make_pattern(resource_format)
        self.amount = amount
        self.resources = self._find_resources()

    @staticmethod
    def _make_pattern(fmt):
        if 'i' not in format_keys(fmt):
            raise ValueError('Resource format {} must contain key "i"'
                             .format(fmt))
        return re.compile('^' + fmt.replace('{i}', '.*') + '$')

    def _find_resources(self):
        return [f for f in os.listdir(self.path)
                if self.pattern.match(f)]

    def __iter__(self):
        resources = cycle(self.resources)
        for _ in range(self.amount):
            filename = next(resources)
            with self.load(filename) as file_:
                yield file_


def get_model(element):
    """Convert element to a Django Model class.

    Element can be a Model class or a DjangoModelFactory class.
    """
    if isinstance(element, FactoryMetaClass):
        return element._meta.model
    if not isinstance(element, ModelBase):
        raise ValueError(
            'Expected Model or DjangoModelFactory, got {}'
            .format(type(element)))
    return element


def watcher(*watched):
    """Decorator to report changes in amounts of objects in a Command.

    Counts number of objects per model before and after the decorated
    function is executed, and shows the difference in nicely formatted
    messages.

    Usage
    -----
    class MyCommand(BaseCommand):

        @watcher(MyModel)
        def do_something(self):
            ... create or delete MyModel instances here ...

    Parameters
    ----------
    *watched :
        List of Model-like (FactoryBoy DjangoModelFactory also accepted).
    """
    watched = list(map(get_model, watched))

    def get_counts():
        return [(model._meta.verbose_name_plural, model.objects.all().count())
                for model in watched]

    def decorator(func):
        def watched_func(self, *args, **kwargs):
            counts_before = get_counts()
            rv = func(self, *args, **kwargs)
            counts_after = get_counts()

            diffs = ((name, after - before)
                     for (name, after), (name, before)
                     in zip(counts_after, counts_before))
            for name, diff in diffs:
                if diff > 0:
                    self.stdout.write(
                        'Created {} {}'.format(diff, name))
                elif diff < 0:
                    self.stdout.write(
                        'Deleted {} {}'.format(-diff, name))
            return rv
        return watched_func
    return decorator
