"""Definition of FieldTestCase and ModelTestCase."""

from django.test import TestCase
from .field_test import FieldTestMeta


class FieldTestCaseMeta(FieldTestMeta):
    """Metaclass for FieldTestCase.

    Dynamically creates tests based on the class' tests dictionary.
    """

    @classmethod
    def dispatch(metacls, cls):
        metacls.dispatch_field(cls, cls.tests, cls.field_name)


class FieldTestCase(TestCase, metaclass=FieldTestCaseMeta):
    """Specialized test case for testing model fields.

    Attributes
    ----------
    model : django.db.Model
    field_name : str
        Name of the field to generate tests for.
    tests : dict
        Define the tested attributes and their expected values here.

    Example usage
    -------------
    class PhoneFieldTestCase(FieldTestCase):
        '''Test phone_number field of User.'''
        model = User
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
            raise TypeError(f'Model not defined in {cls.__name__}')
        if not cls.field_name:
            raise TypeError(f'Field name not defined in {cls.__name__}')


class ModelTestCaseMeta(FieldTestMeta):
    """Metaclass for ModelTestCase.

    Dynamically creates field tests based on the class' field_tests dictionary.
    """

    @classmethod
    def before_dispatch(metacls, cls, name, bases, namespace):
        if not hasattr(cls, 'model'):
            raise ValueError(f'Model not defined for {cls.__name__}')

        if 'tests' in namespace and 'field_tests' not in namespace:
            raise AttributeError(
                'Model field tests should be defined in '
                f'field_tests, not tests (in {cls.__name__})'
            )

    @classmethod
    def dispatch(metacls, cls):
        for field_name, tests in cls.field_tests.items():
            super().dispatch_field(cls, tests, field_name)


class ModelTestCase(TestCase, metaclass=ModelTestCaseMeta):
    """Specialized test case for generic testing of models.

    Attributes
    ----------
    model : django.db.Model
    field_tests : dict
        Used to automatically generate field tests.
        Must map a field name to a dictionary mapping tested field
        attributes to their expected value.

    Example usage
    -------------
    class UserModelTest(ModelTestCase):
        '''Test the User model.'''
        model = User
        field_tests = {
            'email': {'blank': False},
            'phone_number': {'verbose_name': 'téléphone'},
        }
    """

    model = None
    field_tests = {}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.model:
            raise TypeError(f'Model not defined in {cls.__name__}')
