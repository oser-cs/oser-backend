"""Definition of FieldTestCase and ModelTestCase."""

import unittest
from django.db.models.base import ModelBase
from django.db import connection
from django.test import TestCase
from .field_test import FieldTestMeta


__all__ = ('MetaTestCase', 'FieldTestCase', 'ModelTestCase',
           'MixinModelTestCase',)


def run_tests(test_case):
    """Run tests from a test case.

    Returns the TestResults object.
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_case)
    results = unittest.TestResult()
    suite.run(results)
    return results


class MetaTestCase(TestCase):
    """Test case for testing custom test cases.

    Subclasses should define the test_case class attribute.
    """

    test_case = None
    expected_test_methods = []

    def test_created_test_methods(self):
        for method_name in self.expected_test_methods:
            self.assertTrue(hasattr(self.test_case, method_name),
                            msg=method_name)

    def test_execute_generated_methods(self):
        if self.test_case is None:
            return
        results = run_tests(self.test_case)
        self.assertFalse(results.errors or results.failures)


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

    _model_attr_name = 'model'
    _tests_attr_name = 'field_tests'

    @classmethod
    def before_dispatch(metacls, cls, name, bases, namespace):
        model_attr_name_cap = cls._model_attr_name.capitalize()
        if not hasattr(cls, cls._model_attr_name):
            raise AttributeError(f'{model_attr_name_cap} not defined for '
                                 f'{cls.__name__}')

        if 'tests' in namespace and cls._tests_attr_name not in namespace:
            raise AttributeError(
                '{model_attr_name_cap} field tests should be defined in '
                f'{cls._tests_attr_name}, not tests (in {cls.__name__})'
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

    Raises
    ------
    AttributeError : if the ModelTestCase subclass has no model attribute
    """

    model = None
    field_tests = {}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.model:
            raise TypeError(f'Model attribute not defined in {cls.__name__}')


class MixinModelTestCaseMeta(ModelTestCaseMeta):
    """Metaclass for MixinModelTestCase.

    Dynamically creates field tests based on the class' field_tests dictionary.
    """

    _model_attr_name = 'mixin'


class MixinModelTestCase(TestCase, metaclass=MixinModelTestCaseMeta):
    """Base class for tests of model mixins.

    To use, subclass and specify the mixin class variable.
    A model using the mixin will be made available in self.model.

    Inspiration: https://stackoverflow.com/a/45239964

    Attributes
    ----------
    mixin : django.db.Model
    field_tests : dict
        Used to automatically generate field tests.
        See ModelTestCase for more details.

    Raises
    ------
    AttributeError : if the MixinModelTestCase subclass has no mixin attribute
    """

    mixin = None
    field_tests = {}

    @classmethod
    def setUpClass(cls):
        if not cls.mixin:
            raise AttributeError(f'Mixin not defined in {cls.__name__}')
        # Create a dummy model which extends the mixin
        cls.model = ModelBase('__TestModel__' + cls.mixin.__name__,
                              (cls.mixin,),
                              {'__module__': cls.mixin.__module__})

        # Create the schema for our test model
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls.model)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        # Delete the schema for the test model
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(cls.model)
        super().tearDownClass()
