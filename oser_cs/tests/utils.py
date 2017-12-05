"""Generic test function generators and other test utilities."""

import random
from string import ascii_lowercase
from django.test import TestCase


def random_username():
    """Return a random username with 12 lowercase letters."""
    return random.choices(ascii_lowercase, k=12)


def random_email():
    """Return a random email."""
    return '{}@random.net'.format(random.choices(ascii_lowercase, k=12))


class MyTestCase(TestCase):
    """Extends Django's test case with extra assert methods."""

    def get_field(self, obj, field_name):
        """Get a model's field object by name.

        obj : models.Model (class or instance)
        field_name : str
        """
        return obj._meta.get_field(field_name)

    def assertVerboseName(self, model, expected):
        """Compare a model's verbose_name meta attribute to an expected value.

        Parameters
        ---------
        model : models.Model
        expected : str
        """
        name = model._meta.verbose_name
        self.assertEqual(name, expected)

    def assertVerboseNamePlural(self, model, expected):
        """Compare a model's verbose_name_plural meta attr to expected value.

        Parameters
        ---------
        model : models.Model
        expected : str
        """
        name = model._meta.verbose_name_plural
        self.assertEqual(name, expected)

    def assertFieldVerboseName(self, obj, field_name, expected):
        """Compare an object's field verbose_name to an expected value.

        Parameters
        ---------
        obj : models.Model instance
            An instance of a model.
        field_name : str
        expected : str
        """
        name = self.get_field(obj, field_name).verbose_name
        self.assertEqual(name, expected)

    def assertPropertyDescription(self, obj, prop_name, expected):
        """Compare a model's property short_description to an expected value.

        Parameters
        ---------
        obj : models.Model (class or instance)
        prop_name : str
        expected : str
        """
        try:
            prop = obj.__dict__[prop_name]
        except KeyError:
            prop = type(obj).__dict__[prop_name]
        name = prop.fget.short_description
        self.assertEqual(name, expected)

    def assertMaxLength(self, obj, field_name, expected):
        """Compare an object's field max_length to an expected value.

        Typically used on CharFields.

        Parameters
        ---------
        obj : models.Model instance
            An instance of a model.
        field_name : str
            The corresponding field must have a max_length attribute.
        expected : int
        """
        length = self.get_field(obj, field_name).max_length
        self.assertEqual(length, expected)
