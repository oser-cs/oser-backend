"""Test the custom test utilities."""

import unittest
from django.db import models
from django.test import TestCase
from tests.utils import FieldTestCase, ModelTestCase


def run_tests(test_case):
    """Run tests from a test case.

    Returns True if the tests passed (no errors nor failures).
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_case)
    results = unittest.TestResult()
    suite.run(results)
    if results.errors or results.failures:
        return False
    return True


class FieldTestCaseTest(TestCase):
    """Test the usage of FieldTestCase."""

    @classmethod
    def setUpTestData(cls):

        class Article(models.Model):

            title = models.CharField('titre',
                                     max_length=200,
                                     blank=True,
                                     null=True)

            class Meta:  # noqa
                app_label = 'tests'

        cls.model = Article

        class TitleFieldTestCase(FieldTestCase):
            model = cls.model
            field_name = 'title'
            tests = {
                'verbose_name': 'titre',
                'max_length': 200,
                'blank': True,
                'null': True,
                'unique': False,
            }

        cls.test_case = TitleFieldTestCase

    def test_created_test_methods(self):
        method_names = [
            'test_title_verbose_name',
            'test_title_max_length_value',
            'test_title_blank_is_true',
            'test_title_null_is_true',
            'test_title_unique_is_false',
        ]
        for method_name in method_names:
            self.assertTrue(hasattr(self.test_case, method_name),
                            msg=method_name)

    def test_execute_generated_methods(self):
        self.assertTrue(run_tests(self.test_case))


class ModelTestCaseTest(TestCase):
    """Test the usage of ModelTestCase."""

    @classmethod
    def setUpTestData(cls):

        class Album(models.Model):

            title = models.CharField('titre',
                                     max_length=200,
                                     blank=True,
                                     null=True)
            is_published = models.BooleanField('publié')

            class Meta:  # noqa
                app_label = 'tests'

        cls.model = Album

        class AlbumTestCase(ModelTestCase):
            model = cls.model
            field_tests = {
                'title': {
                    'verbose_name': 'titre',
                    'max_length': 200,
                    'blank': True,
                    'null': True,
                    'unique': False,
                },
                'is_published': {
                    'verbose_name': 'publié',
                }
            }

        cls.test_case = AlbumTestCase

    def test_created_test_methods(self):
        method_names = [
            'test_title_verbose_name',
            'test_title_max_length_value',
            'test_title_blank_is_true',
            'test_title_null_is_true',
            'test_title_unique_is_false',
            'test_is_published_verbose_name',
        ]
        for method_name in method_names:
            self.assertTrue(hasattr(self.test_case, method_name),
                            msg=method_name)

    def test_execute_generated_methods(self):
        self.assertTrue(run_tests(self.test_case))
