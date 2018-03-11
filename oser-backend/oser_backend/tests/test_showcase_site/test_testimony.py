"""Testimony model tests."""
import showcase_site.models
from showcase_site.factory import TestimonyFactory
from tests.utils import ModelTestCase


class TestimonyTest(ModelTestCase):
    """Test the Testimony model."""

    model = showcase_site.models.Testimony
    field_tests = {
        'created': {
            'verbose_name': 'date de création',
        },
        'author_name': {
            'max_length': 300,
            'verbose_name': 'auteur',
        },
        'author_position': {
            'verbose_name': 'position',
        },
        'author': {
            'short_description': 'auteur',
        },
        'content': {
            'verbose_name': 'contenu',
        },
    }
    model_tests = {
        'verbose_name': 'témoignage',
        'ordering': ('-created', 'author_name'),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj = TestimonyFactory.create()

    def test_author_property_is_author_name_comma_position_lower(self):
        expected = '{}, {}'.format(self.obj.author_name,
                                   self.obj.author_position.lower())
        self.assertEqual(self.obj.author, expected)
