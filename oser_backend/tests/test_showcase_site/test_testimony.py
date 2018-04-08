"""Testimony model tests."""
import showcase_site.models
from showcase_site.factory import TestimonyFactory
from tests.utils import ModelTestCase


class TestimonyTest(ModelTestCase):
    """Test the Testimony model."""

    model = showcase_site.models.Testimony
    field_tests = {
        'created': {
            'verbose_name': 'ajouté le',
        },
        'source': {
            'max_length': 300,
        },
        'quote': {
            'verbose_name': 'citation',
        },
    }
    model_tests = {
        'verbose_name': 'témoignage',
        'ordering': ('-created', 'source'),
    }

    @classmethod
    def setUpTestData(cls):
        cls.obj: showcase_site.models.Testimony = TestimonyFactory.create()

    def test_preview_is_40_characters_max(self):
        quote = self.obj.quote
        max_len = self.obj.PREVIEW_LENGTH
        expected = (len(quote) > max_len) and quote[:max_len] + '...' or quote
        self.assertEqual(expected, self.obj.preview)
