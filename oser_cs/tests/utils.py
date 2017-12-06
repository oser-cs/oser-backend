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


class FieldTestCaseMeta(type):
    """Metaclass for FieldTestCase.

    Dynamically creates tests based on the class' tests dictionary.
    """

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        for attr, value in cls.tests.items():
            if isinstance(value, bool):
                type(cls).add_bool_test_method(cls, attr, value)
            else:
                raise ValueError(f'Unsupported test: {attr}, {value}')

    @classmethod
    def add_bool_test_method(metacls, cls, attr, value):
        if value is True:
            def test_bool(self):
                self.assertTrue(getattr(self.field, attr))
        else:
            def test_bool(self):
                self.assertFalse(getattr(self.field, attr))
        method_name = f'test_{attr}_is_{value}'.lower()
        test_bool.__name__ = method_name
        setattr(cls, method_name, test_bool)


class FieldTestCase(TestCase, metaclass=FieldTestCaseMeta):
    """Specialized test case for testing model fields.

    Example
    -------
    class PhoneFieldTestCase(FieldTestCase):
        model = PhoneNumber
        field_name = 'phone_number'
        tests = {
            'blank': True,
            'unique': False,
        }
    """

    model = None
    field_name = None
    tests = {}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.model:
            raise TypeError(f'Model not declared in {cls.__name__}')
        if not cls.field_name:
            raise TypeError(f'Field name not declared in {cls.__name__}')

    def setUp(self):
        self.field = self.model._meta.get_field(self.field_name)
