"""Test the custom test utilities."""
from django.db import models
from django.test import TestCase
from tests.utils import FieldTestCase, ModelTestCase, MixinModelTestCase
from tests.utils import MetaTestCase


class FieldTestCaseTest(MetaTestCase):
    """Test the usage of FieldTestCase."""

    expected_test_methods = [
        'test_title_verbose_name',
        'test_title_max_length_value',
        'test_title_blank_is_true',
        'test_title_null_is_true',
        'test_title_unique_is_false',
    ]

    @classmethod
    def setUpTestData(cls):

        class Article(models.Model):
            """Dummy model."""

            title = models.CharField('titre',
                                     max_length=200,
                                     blank=True,
                                     null=True)

            class Meta:  # noqa
                app_label = 'tests'

        class TitleFieldTestCase(FieldTestCase):
            model = Article
            field_name = 'title'
            tests = {
                'verbose_name': 'titre',
                'max_length': 200,
                'blank': True,
                'null': True,
                'unique': False,
            }

        cls.test_case = TitleFieldTestCase


class ModelTestCaseTest(MetaTestCase):
    """Test the usage of ModelTestCase."""

    expected_test_methods = [
        'test_title_verbose_name',
        'test_title_max_length_value',
        'test_title_blank_is_true',
        'test_title_null_is_true',
        'test_title_unique_is_false',
        'test_is_published_verbose_name',
    ]

    @classmethod
    def setUpTestData(cls):

        class Album(models.Model):
            """Dummy model."""

            title = models.CharField('titre',
                                     max_length=200,
                                     blank=True,
                                     null=True)
            is_published = models.BooleanField('publié')

            class Meta:  # noqa
                app_label = 'tests'

        class AlbumTestCase(ModelTestCase):
            model = Album
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


class MixinModelTestCaseTest(TestCase):
    """Test the usage of MixinModelTestCase."""

    expected_test_methods = [
        'test_name_verbose_name',
        'test_name_max_length_value',
    ]

    @classmethod
    def setUpTestData(cls):

        class Place(models.Model):
            """Dummy abstract model (mixin)."""

            name = models.CharField('nom', max_length=200)

            class Meta:  # noqa
                app_label = 'tests'
                abstract = True

        class PlaceTestCase(MixinModelTestCase):
            mixin = Place
            field_tests = {
                'name': {
                    'verbose_name': 'nom',
                    'max_length': 200,
                },
            }

        cls.test_case = PlaceTestCase
