"""Definition of FieldTestCase and ModelTestCase."""

import unittest

from django.db import connection
from django.db.models.base import ModelBase
from django.test import TestCase

from .field_test import ModelTestCaseMeta

__all__ = ('MetaTestCase', 'ModelTestCase', 'MixinModelTestCase',)


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

    Attributes
    ----------
    test_case : subclass of TestCase
        The test case to test.
    execute_test_case : bool, default is True
        If True, the test_case will be executed and checked for errors
        and failures.
    expected_test_methods : list of str
        List of test methods that should be found on test_case.
    """

    test_case = None
    execute_test_case = True
    expected_test_methods = []

    def test_created_test_methods(self):
        for method_name in self.expected_test_methods:
            self.assertTrue(hasattr(self.test_case, method_name),
                            msg=method_name)

    def test_execute_generated_methods(self):
        if self.test_case is None or not self.execute_test_case:
            return
        results = run_tests(self.test_case)
        self.assertFalse(results.errors or results.failures)


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
        model_tests = {
            'verbose_name': 'utilisateur',
            'order_by': ('last_name', 'first_name'),
        }

    Raises
    ------
    AttributeError : if the ModelTestCase subclass has no model attribute
    """

    model = None
    field_tests = {}
    model_tests = {}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.model:
            raise TypeError('model not declared on {}'
                            .format(cls.__name__))


class MixinModelTestCaseMeta(ModelTestCaseMeta):
    """Metaclass for MixinModelTestCase.

    Dynamically creates field and model tests based on the class'
    field_tests and model_tests dictionary.
    """

    model_attr_name = 'mixin'


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
    model_tests = {}

    @classmethod
    def setUpClass(cls):
        if not cls.mixin:
            raise AttributeError('Mixin not defined in {}'
                                 .format(cls.__name__))
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
