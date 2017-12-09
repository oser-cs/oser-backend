"""Definition of FieldTestCase.

Usage
-----
class PhoneFieldTestCase(FieldTestCase):
    '''Test phone_number field of User.'''
    model = User
    field_name = 'phone_number'
    tests = {
        'verbose_name': 'numéro de téléphone',
        'blank': True,
        'unique': False,
    }


Supported attribute tests
-------------------------
Boolean value test:
    'unique': True
String equality test:
    'verbose_name': 'my-field-verbose-name'
"""

from django.test import TestCase


class FieldTestMethodMeta(type):
    """Meta FieldTestMethod class to hold all created field test methods."""

    CLASSES = []

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if name != 'FieldTestMethod':
            type(cls).CLASSES.append(cls)


class FieldTestMethod(metaclass=FieldTestMethodMeta):
    """Field test method factory.

    Use .create(attr, value) to create a test method for a specific
    (attr, value) pair.
    """

    name_formatter = None

    @classmethod
    def create(cls, attr, value):
        if not cls.name_formatter:
            raise ValueError(f'Name formatter not defined for {cls.__name__}')
        test_method = cls.get_test_method(attr, value)
        test_method.__name__ = cls.name_formatter.format(
            attr=attr, value=value)
        return test_method

    @classmethod
    def get_test_method(cls, attr, value):
        raise NotImplementedError

    @classmethod
    def accepts(cls, attr, value):
        raise NotImplementedError

    @staticmethod
    def all():
        """Return the list of available field test methods."""
        return FieldTestMethodMeta.CLASSES

    @staticmethod
    def name_from_func(f):
        words = f.__name__.split('_')
        name = ''.join(word.capitalize() for word in words)
        return '{}FieldTestMethod'.format(name)


def field_test_method(name_formatter=None, accept=None):
    """Decorator to easily create field test methods."""
    if accept is None:
        def accept(attr, value):
            return True

    def create_test_method(f):
        formatter = name_formatter

        class MyFieldTestMethod(FieldTestMethod):

            name_formatter = formatter

            @classmethod
            def get_test_method(cls, attr, value):
                def test_method(self):
                    f(self, attr, value)
                return test_method

            @classmethod
            def accepts(cls, attr, value):
                return accept(attr, value)

        MyFieldTestMethod.__name__ = FieldTestMethod.name_from_func(f)

    return create_test_method


@field_test_method(name_formatter='test_{attr}_is_{value}',
                   accept=lambda attr, value: isinstance(value, bool))
def test_bool(self, attr, value):
    """Test that a field attribute is True or False according to value."""
    if value is True:
        self.assertTrue(getattr(self.field, attr))
    else:
        self.assertFalse(getattr(self.field, attr))


@field_test_method(name_formatter='test_{attr}_value',
                   accept=lambda attr, value: isinstance(value, str))
def test_string_equals(self, attr, value):
    """Test that a field attribute is the given string value."""
    self.assertEqual(getattr(self.field, attr), value)


class FieldTestCaseMeta(type):
    """Metaclass for FieldTestCase.

    Dynamically creates tests based on the class' tests dictionary.
    """

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        for attr, value in cls.tests.items():
            added = type(cls).add_test_method(cls, attr, value)
            if not added:
                raise ValueError(f'Unsupported test: {attr}')

    @classmethod
    def add_test_method(metacls, cls, attr, value):
        for test_method_cls in FieldTestMethod.all():
            if test_method_cls.accepts(attr, value):
                test_method = test_method_cls.create(attr, value)
                setattr(cls, test_method.__name__, test_method)
                return True
        return False


class FieldTestCase(TestCase, metaclass=FieldTestCaseMeta):
    """Specialized test case for testing model fields.

    Example
    -------
    class PhoneFieldTestCase(FieldTestCase):
        model = PhoneNumber
        field_name = 'phone_number'
        tests = {
            'verbose_name': 'numéro de téléphone',
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
